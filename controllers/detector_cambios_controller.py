import json
import os
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from models.detector_cambios_models import CompareCambioBatchResponse, CompareCambioResponse
from orchestrators.detector_cambios_orchestrator import DetectorCambiosOrchestrator
from preservices.preservice_filemanager import PreserviceFileManager
from services.detector_cambios_service.artifact_archive_service import ArtifactArchiveService
from services.detector_cambios_service.config_loader_service import ConfigLoaderService
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
config_loader_service = ConfigLoaderService()
file_manager = PreserviceFileManager()

MODEL_NAME = "control_cambios"
TRAINING_DATASET_PATH = os.path.join("data", "generador_nlp", "datasets", "control_cambios_augmentado.csv")


def _load_artifacts_from_archive(archive_bytes: bytes) -> None:
    try:
        model_bytes = archive_service.extract(archive_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    pipeline = persistence_service.load(model_bytes)
    detector_cambios_service.load_artifacts(pipeline)


@router.post("/train_detector_cambios")
async def train_detector_cambios():
    if not os.path.exists(TRAINING_DATASET_PATH):
        raise HTTPException(status_code=500, detail=f"No se encontró el dataset de entrenamiento en '{TRAINING_DATASET_PATH}'.")

    trained = detector_cambios_orchestrator.run(TRAINING_DATASET_PATH, config_loader_service.load())

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
    return render_compare_response(
        phrase, resultado["es_conocida"], resultado["distancia"], resultado["frase_mas_parecida"]
    )


@router.post("/compare_cambio_batch", response_model=CompareCambioBatchResponse)
async def compare_cambio_batch(file: UploadFile, artifacts: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()
    if extension != ".csv":
        raise HTTPException(status_code=400, detail="Se esperaba un archivo CSV.")

    archive_bytes = await artifacts.read()
    _load_artifacts_from_archive(archive_bytes)

    contents = await file.read()
    with file_manager.temp_input_file(contents, extension) as csv_path:
        resultados = detector_cambios_batch_service.compare_from_csv(csv_path, detector_cambios_service.pipeline)

    return render_compare_batch_response(resultados)
