from pydantic import BaseModel


class ClassifyTextResponse(BaseModel):
    frase: str
    etiqueta: str
    confianza: float
    terminos_clave: list[str] = []


class ClassifyTextBatchResponse(BaseModel):
    predicciones: list[ClassifyTextResponse]
