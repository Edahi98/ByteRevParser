from models.text_classifier_models import ClassifyTextBatchResponse, ClassifyTextResponse


def render_classify_response(phrase: str, etiqueta: str, confianza: float) -> ClassifyTextResponse:
    return ClassifyTextResponse(frase=phrase, etiqueta=etiqueta, confianza=confianza)


def render_classify_batch_response(predicciones: list[dict]) -> ClassifyTextBatchResponse:
    return ClassifyTextBatchResponse(predicciones=predicciones)
