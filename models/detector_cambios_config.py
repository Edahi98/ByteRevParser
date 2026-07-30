from pydantic import BaseModel, Field


class TfidfConfig(BaseModel):
    analyzer: str = "char_wb"
    ngram_range: tuple[int, int] = (3, 5)
    max_features: int = 20000


class SiameseConfig(BaseModel):
    hidden_dim: int = 256
    embedding_dim: int = 100
    margin: float = 1.0
    epochs: int = 20
    batch_size: int = 64
    learning_rate: float = 0.001
    pairs_per_anchor: int = 2


class DetectorCambiosConfig(BaseModel):
    random_seed: int = 42
    tfidf: TfidfConfig = Field(default_factory=TfidfConfig)
    siamese: SiameseConfig = Field(default_factory=SiameseConfig)
