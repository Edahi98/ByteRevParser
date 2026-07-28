from pydantic import BaseModel, Field


class TfidfConfig(BaseModel):
    ngram_range: tuple[int, int] = (1, 3)
    max_features: int = 5000


class Word2VecConfig(BaseModel):
    vector_size: int = 100
    window: int = 5
    min_count: int = 2
    sg: int = 1


class CalibrationConfig(BaseModel):
    method: str = "sigmoid"
    folds: int = 3


class EvaluationConfig(BaseModel):
    cv_folds: int = 5


class ClassifiersConfig(BaseModel):
    class_weight: str = "balanced"


class ClassificationConfig(BaseModel):
    confidence_threshold: float = 0.5
    high_confidence_override: float = 0.85


class TextClassifierConfig(BaseModel):
    random_seed: int = 42
    tfidf: TfidfConfig = Field(default_factory=TfidfConfig)
    word2vec: Word2VecConfig = Field(default_factory=Word2VecConfig)
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    classifiers: ClassifiersConfig = Field(default_factory=ClassifiersConfig)
    classification: ClassificationConfig = Field(default_factory=ClassificationConfig)
