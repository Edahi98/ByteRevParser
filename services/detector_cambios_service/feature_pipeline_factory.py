from typing import Callable

from sklearn.pipeline import Pipeline

from models.detector_cambios_config import DetectorCambiosConfig
from services.detector_cambios_service.char_tokenizer import CharTokenizer
from services.detector_cambios_service.detector_cambios_encoder import DetectorCambiosEncoder


class FeaturePipelineFactory:
    """Construye el pipeline de features: secuencias de caracteres reducidas por un Transformer entrenado desde cero.

    Un `staticmethod` en vez de una función suelta, siguiendo el mismo
    patrón de fábrica que `BinaryAdapterFactory`. `CharTokenizer`
    convierte cada frase en una secuencia de índices de caracteres (no
    una bolsa de fragmentos fija) y `DetectorCambiosEncoder` aprende de
    punta a punta, con auto-atención, cómo combinarlos en un embedding
    denso — entrenado con pérdida contrastiva para que frases de control
    de cambios equivalentes queden cerca y frases distintas queden lejos.
    Todos los hiperparámetros vienen de `DetectorCambiosConfig`.
    """

    @staticmethod
    def create(config: DetectorCambiosConfig, progress_callback: Callable[[int, int], None] | None = None) -> Pipeline:
        return Pipeline([
            (
                "tokenizer",
                CharTokenizer(
                    max_length=config.tokenizer.max_length,
                    lowercase=config.tokenizer.lowercase,
                ),
            ),
            (
                "encoder",
                DetectorCambiosEncoder(
                    embed_dim=config.siamese.embed_dim,
                    num_layers=config.siamese.num_layers,
                    num_heads=config.siamese.num_heads,
                    ff_dim=config.siamese.ff_dim,
                    embedding_dim=config.siamese.embedding_dim,
                    max_length=config.tokenizer.max_length,
                    dropout=config.siamese.dropout,
                    margin=config.siamese.margin,
                    epochs=config.siamese.epochs,
                    batch_size=config.siamese.batch_size,
                    learning_rate=config.siamese.learning_rate,
                    pairs_per_anchor=config.siamese.pairs_per_anchor,
                    seed=config.random_seed,
                    progress_callback=progress_callback,
                ),
            ),
        ])
