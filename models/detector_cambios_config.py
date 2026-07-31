from pydantic import BaseModel, Field


class TokenizerConfig(BaseModel):
    max_length: int = 160
    lowercase: bool = True


class SiameseConfig(BaseModel):
    embed_dim: int = 64
    num_layers: int = 3
    num_heads: int = 4
    ff_dim: int = 128
    embedding_dim: int = 100
    dropout: float = 0.1
    margin: float = 1.0
    epochs: int = 20
    batch_size: int = 64
    learning_rate: float = 0.001
    pairs_per_anchor: int = 2


class DetectorCambiosConfig(BaseModel):
    random_seed: int = 42
    tokenizer: TokenizerConfig = Field(default_factory=TokenizerConfig)
    siamese: SiameseConfig = Field(default_factory=SiameseConfig)
