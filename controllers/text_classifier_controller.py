import json
import re
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from models.text_classifier_models import ClassifyTextBatchResponse, ClassifyTextResponse
from orchestrators.text_classifier_orchestrator import TextClassifierOrchestrator
from preservices.preservice_filemanager import PreserviceFileManager
from services.text_classifier.artifact_archive_service import ArtifactArchiveService
from services.text_classifier.config_loader_service import ConfigLoaderService
from services.text_classifier.config_override_service import ConfigOverrideService
from services.text_classifier.model_persistence_service import ModelPersistenceService
from services.text_classifier.predictor_service import PredictorService
from services.text_classifier.text_classification_service import TextClassificationService
from views.text_classifier_view import render_classify_batch_response, render_classify_response

router = APIRouter()

text_classifier_orchestrator = TextClassifierOrchestrator()
text_classification_service = TextClassificationService()
predictor_service = PredictorService()
persistence_service = ModelPersistenceService()
archive_service = ArtifactArchiveService()
config_loader_service = ConfigLoaderService()
config_override_service = ConfigOverrideService()
file_manager = PreserviceFileManager()

DEFAULT_MODEL_NAME = "text_classifier"
INVALID_MODEL_NAME_CHARS = re.compile(r"[^A-Za-z0-9_-]+")


def _sanitize_model_name(model_name: str) -> str:
    sanitized = INVALID_MODEL_NAME_CHARS.sub("_", model_name.strip())
    return sanitized or DEFAULT_MODEL_NAME


def _resolve_config(config_json: str | None):
    base_config = config_loader_service.load()
    if not config_json:
        return base_config

    try:
        overrides = json.loads(config_json)
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=400, detail="El JSON de configuración no es válido.") from error

    try:
        return config_override_service.apply(base_config, overrides)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Configuración inválida: {error}") from error


def _load_artifacts_from_archive(archive_bytes: bytes) -> None:
    try:
        model_bytes, novelty_bytes = archive_service.extract(archive_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    pipeline = persistence_service.load(model_bytes)
    novelty_pipeline = persistence_service.load(novelty_bytes)
    text_classification_service.load_artifacts(pipeline, novelty_pipeline)


@router.post("/train_text_classifier")
async def train_text_classifier(
    file: UploadFile, model_name: str = Form(DEFAULT_MODEL_NAME), config: str | None = Form(None)
):
    extension = Path(file.filename or "").suffix.lower()
    if extension != ".csv":
        raise HTTPException(status_code=400, detail="Se esperaba un archivo CSV.")

    model_name = _sanitize_model_name(model_name)
    resolved_config = _resolve_config(config)

    contents = await file.read()
    with file_manager.temp_input_file(contents, extension) as csv_path:
        trained = text_classifier_orchestrator.run(csv_path, resolved_config)

    model_bytes = persistence_service.dump(trained["model"])
    novelty_bytes = persistence_service.dump(trained["novelty_model"])
    report_bytes = json.dumps(trained["report"], ensure_ascii=False).encode("utf-8")

    archive_bytes = archive_service.build(model_name, model_bytes, novelty_bytes, report_bytes)

    return Response(
        content=archive_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{model_name}.zip"'},
    )


@router.post("/classify_text", response_model=ClassifyTextResponse)
async def classify_text(phrase: str = Form(...), artifacts: UploadFile = File(...)):
    archive_bytes = await artifacts.read()
    _load_artifacts_from_archive(archive_bytes)

    resultado = text_classification_service.classify(phrase)
    return render_classify_response(phrase, resultado["etiqueta"], resultado["confianza"], resultado["terminos_clave"])


@router.post("/classify_text_batch", response_model=ClassifyTextBatchResponse)
async def classify_text_batch(file: UploadFile, artifacts: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()
    if extension != ".csv":
        raise HTTPException(status_code=400, detail="Se esperaba un archivo CSV.")

    archive_bytes = await artifacts.read()
    _load_artifacts_from_archive(archive_bytes)

    contents = await file.read()
    with file_manager.temp_input_file(contents, extension) as csv_path:
        predicciones = predictor_service.predict_from_csv(
            csv_path, text_classification_service.pipeline, text_classification_service.novelty_pipeline
        )

    return render_classify_batch_response(predicciones)
