import json
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from controllers.large_multipart_route import LargeMultipartRoute
from models.pipeline_models import PipelineResponse
from orchestrators.ocr_orchestrator import OcrOrchestrator
from orchestrators.xml_orchestrator import ALLOWED_EXTENSIONS
from preservices.preservice_filemanager import PreserviceFileManager
from views.pipeline_view import render_pipeline_response

router = APIRouter(route_class=LargeMultipartRoute)

ocr_orchestrator = OcrOrchestrator()
file_manager = PreserviceFileManager()


@router.post("/execute_pipeline", response_model=PipelineResponse)
async def execute_pipeline(
    file: UploadFile,
    pipeline: str = Form(...),
    schema: str = Form(...),
    artifacts: UploadFile = File(...),
):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{extension}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    pipeline_data = json.loads(pipeline)
    schema_data = json.loads(schema)
    contents = await file.read()
    artifacts_bytes = await artifacts.read()

    try:
        with file_manager.temp_input_file(contents, extension) as input_path:
            result = ocr_orchestrator.run(input_path, pipeline_data, schema_data, artifacts_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return render_pipeline_response(file.filename, result)
