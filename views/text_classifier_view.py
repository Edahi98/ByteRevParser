from models.text_classifier_models import ClassifyTextBatchResponse, ClassifyTextResponse


def render_classify_response(phrase: str, etiqueta: str, confianza: float, terminos_clave: list[str]) -> ClassifyTextResponse:
    return ClassifyTextResponse(frase=phrase, etiqueta=etiqueta, confianza=confianza, terminos_clave=terminos_clave)


def render_classify_batch_response(predicciones: list[dict]) -> ClassifyTextBatchResponse:
    return ClassifyTextBatchResponse(predicciones=predicciones)
