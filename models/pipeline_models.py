from pydantic import BaseModel


class PipelineResponse(BaseModel):
    filename: str
    result: dict
