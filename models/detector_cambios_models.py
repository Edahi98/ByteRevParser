from pydantic import BaseModel


class CompareCambioResponse(BaseModel):
    frase: str
    es_conocida: bool
    distancia: float
    frase_mas_parecida: str


class CompareCambioBatchResponse(BaseModel):
    resultados: list[CompareCambioResponse]
