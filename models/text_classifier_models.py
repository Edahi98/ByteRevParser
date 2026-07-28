from pydantic import BaseModel


class ClassDistribution(BaseModel):
    etiqueta: str
    conteo: int


class ModelEvaluationResult(BaseModel):
    f1_macro_por_fold: list[float]
    f1_macro_promedio: float
    f1_macro_desviacion: float
    classification_report: dict


class TrainTextClassifierResponse(BaseModel):
    clases: list[ClassDistribution]
    resultados_cv: dict[str, ModelEvaluationResult]


class ClassifyTextResponse(BaseModel):
    frase: str
    etiqueta: str


class ClassifyTextBatchResponse(BaseModel):
    predicciones: list[ClassifyTextResponse]
