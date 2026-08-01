from models.detector_cambios_models import CompareCambioBatchResponse, CompareCambioResponse


def render_compare_response(phrase: str, es_cambio: bool, probabilidad: float) -> CompareCambioResponse:
    return CompareCambioResponse(frase=phrase, es_cambio=es_cambio, probabilidad=probabilidad)


def render_compare_batch_response(resultados: list[dict]) -> CompareCambioBatchResponse:
    return CompareCambioBatchResponse(resultados=resultados)
