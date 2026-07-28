from models.text_classifier_models import (
    ClassifyTextBatchResponse,
    ClassifyTextResponse,
    TrainTextClassifierResponse,
)


def render_train_response(report: dict) -> TrainTextClassifierResponse:
    return TrainTextClassifierResponse(clases=report["clases"], resultados_cv=report["resultados_cv"])


def render_classify_response(phrase: str, etiqueta: str) -> ClassifyTextResponse:
    return ClassifyTextResponse(frase=phrase, etiqueta=etiqueta)


def render_classify_batch_response(predicciones: list[dict]) -> ClassifyTextBatchResponse:
    return ClassifyTextBatchResponse(predicciones=predicciones)
