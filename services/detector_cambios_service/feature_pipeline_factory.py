from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

from models.detector_cambios_config import DetectorCambiosConfig
from services.detector_cambios_service.detector_cambios_encoder import DetectorCambiosEncoder


class FeaturePipelineFactory:
    """Construye el pipeline de features: TF-IDF de n-gramas de caracteres reducido con una red siamesa.

    Un `staticmethod` en vez de una función suelta, siguiendo el mismo
    patrón de fábrica que `BinaryAdapterFactory`. `analyzer='char_wb'`
    vectoriza por n-gramas de caracteres dentro de cada palabra en vez de
    por palabra completa, lo que tolera errores de ortografía sin
    necesitar que la palabra esté escrita igual que en entrenamiento.
    `DetectorCambiosEncoder` (PyTorch) reduce ese espacio disperso a un
    embedding denso entrenado con pérdida contrastiva, para que frases de
    control de cambios equivalentes queden cerca y frases distintas
    queden lejos. Todos los hiperparámetros vienen de `DetectorCambiosConfig`.
    """

    @staticmethod
    def create(config: DetectorCambiosConfig) -> Pipeline:
        return Pipeline([
            (
                "vectorizer",
                TfidfVectorizer(
                    analyzer=config.tfidf.analyzer,
                    ngram_range=config.tfidf.ngram_range,
                    max_features=config.tfidf.max_features,
                ),
            ),
            ("normalize", Normalizer()),
            (
                "encoder",
                DetectorCambiosEncoder(
                    hidden_dim=config.siamese.hidden_dim,
                    embedding_dim=config.siamese.embedding_dim,
                    margin=config.siamese.margin,
                    epochs=config.siamese.epochs,
                    batch_size=config.siamese.batch_size,
                    learning_rate=config.siamese.learning_rate,
                    pairs_per_anchor=config.siamese.pairs_per_anchor,
                    seed=config.random_seed,
                ),
            ),
        ])
