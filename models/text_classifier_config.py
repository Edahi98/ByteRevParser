from pydantic import BaseModel, Field


class TfidfConfig(BaseModel):
    analyzer: str = "char_wb"
    ngram_range: tuple[int, int] = (3, 5)
    max_features: int = 20000


class AutoencoderConfig(BaseModel):
    hidden_dim: int = 256
    bottleneck_dim: int = 100
    epochs: int = 15
    batch_size: int = 64
    learning_rate: float = 0.001


class ClusteringConfig(BaseModel):
    k_min: int = 2
    k_max: int = 15


class NoveltyConfig(BaseModel):
    contamination: float | str = 0.05


class TextClassifierConfig(BaseModel):
    random_seed: int = 42
    tfidf: TfidfConfig = Field(default_factory=TfidfConfig)
    autoencoder: AutoencoderConfig = Field(default_factory=AutoencoderConfig)
    clustering: ClusteringConfig = Field(default_factory=ClusteringConfig)
    novelty: NoveltyConfig = Field(default_factory=NoveltyConfig)
