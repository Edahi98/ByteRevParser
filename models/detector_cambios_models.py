from pydantic import BaseModel


class CompareCambioResponse(BaseModel):
    frase: str
    es_cambio: bool
    probabilidad: float


class CompareCambioBatchResponse(BaseModel):
    resultados: list[CompareCambioResponse]
