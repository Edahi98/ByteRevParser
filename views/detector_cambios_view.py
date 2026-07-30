from models.detector_cambios_models import CompareCambioBatchResponse, CompareCambioResponse


def render_compare_response(phrase: str, es_conocida: bool, distancia: float, frase_mas_parecida: str) -> CompareCambioResponse:
    return CompareCambioResponse(
        frase=phrase, es_conocida=es_conocida, distancia=distancia, frase_mas_parecida=frase_mas_parecida
    )


def render_compare_batch_response(resultados: list[dict]) -> CompareCambioBatchResponse:
    return CompareCambioBatchResponse(resultados=resultados)
