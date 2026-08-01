from models.pipeline_models import PipelineResponse


def render_pipeline_response(filename: str, result: dict) -> PipelineResponse:
    return PipelineResponse(filename=filename, result=result)
