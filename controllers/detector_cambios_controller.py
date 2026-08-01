import json
import os
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from models.detector_cambios_models import CompareCambioBatchResponse, CompareCambioResponse
from orchestrators.detector_cambios_orchestrator import DetectorCambiosOrchestrator
from preservices.preservice_filemanager import PreserviceFileManager
from services.detector_cambios_service.artifact_archive_service import ArtifactArchiveService
from services.detector_cambios_service.dataset_service import CALIDAD_PATH, CAMBIOS_PATH
from services.detector_cambios_service.detector_cambios_batch_service import DetectorCambiosBatchService
from services.detector_cambios_service.detector_cambios_service import DetectorCambiosService
from services.detector_cambios_service.model_persistence_service import ModelPersistenceService
from views.detector_cambios_view import render_compare_batch_response, render_compare_response

router = APIRouter()

detector_cambios_orchestrator = DetectorCambiosOrchestrator()
detector_cambios_service = DetectorCambiosService()
detector_cambios_batch_service = DetectorCambiosBatchService()
persistence_service = ModelPersistenceService()
archive_service = ArtifactArchiveService()
file_manager = PreserviceFileManager()

MODEL_NAME = "control_cambios"


def _load_artifacts_from_archive(archive_bytes: bytes) -> None:
    try:
        model_bytes = archive_service.extract(archive_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    encoder = persistence_service.load(model_bytes)
    detector_cambios_service.load_artifacts(encoder)


@router.post("/train_detector_cambios")
async def train_detector_cambios():
    if not os.path.exists(CAMBIOS_PATH) or not os.path.exists(CALIDAD_PATH):
        raise HTTPException(
            status_code=500, detail=f"No se encontraron los datasets de entrenamiento en '{CAMBIOS_PATH}' y '{CALIDAD_PATH}'."
        )

    trained = detector_cambios_orchestrator.run()

    model_bytes = persistence_service.dump(trained["model"])
    report_bytes = json.dumps(trained["report"], ensure_ascii=False).encode("utf-8")
    archive_bytes = archive_service.build(model_bytes, report_bytes)

    return Response(
        content=archive_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{MODEL_NAME}.zip"'},
    )


@router.post("/compare_cambio", response_model=CompareCambioResponse)
async def compare_cambio(phrase: str = Form(...), artifacts: UploadFile = File(...)):
    archive_bytes = await artifacts.read()
    _load_artifacts_from_archive(archive_bytes)

    resultado = detector_cambios_service.compare(phrase)
    return render_compare_response(phrase, resultado["es_cambio"], resultado["probabilidad"])


@router.post("/compare_cambio_batch", response_model=CompareCambioBatchResponse)
async def compare_cambio_batch(file: UploadFile, artifacts: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()
    if extension != ".csv":
        raise HTTPException(status_code=400, detail="Se esperaba un archivo CSV.")

    archive_bytes = await artifacts.read()
    _load_artifacts_from_archive(archive_bytes)

    contents = await file.read()
    with file_manager.temp_input_file(contents, extension) as csv_path:
        resultados = detector_cambios_batch_service.compare_from_csv(csv_path, detector_cambios_service.encoder)

    return render_compare_batch_response(resultados)
