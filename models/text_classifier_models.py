from pydantic import BaseModel


class ClassifyTextResponse(BaseModel):
    frase: str
    etiqueta: str
    confianza: float


class ClassifyTextBatchResponse(BaseModel):
    predicciones: list[ClassifyTextResponse]
