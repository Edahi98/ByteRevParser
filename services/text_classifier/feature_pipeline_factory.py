from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

from models.text_classifier_config import TextClassifierConfig
from services.text_classifier.autoencoder_embedder import AutoencoderEmbedder


class FeaturePipelineFactory:
    """Construye el pipeline de features: TF-IDF de n-gramas de caracteres reducido con un autoencoder.

    Un `staticmethod` en vez de una función suelta, siguiendo el mismo
    patrón de fábrica que `BinaryAdapterFactory`. `analyzer='char_wb'`
    vectoriza por n-gramas de caracteres dentro de cada palabra en vez de
    por palabra completa, lo que tolera errores de ortografía y ruido de
    OCR/tipeo sin necesitar que la palabra esté escrita igual que en
    entrenamiento. `AutoencoderEmbedder` (PyTorch) reduce ese espacio
    disperso a uno denso y de baja dimensión de forma no lineal —
    aprendida por backpropagation, no una proyección lineal fija como
    `TruncatedSVD` — más estable para KMeans e IsolationForest, y que de
    paso aporta el error de reconstrucción como señal extra de ruido.
    Todos los hiperparámetros vienen de `TextClassifierConfig`.
    """

    @staticmethod
    def create(config: TextClassifierConfig) -> Pipeline:
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
                "embedder",
                AutoencoderEmbedder(
                    hidden_dim=config.autoencoder.hidden_dim,
                    bottleneck_dim=config.autoencoder.bottleneck_dim,
                    epochs=config.autoencoder.epochs,
                    batch_size=config.autoencoder.batch_size,
                    learning_rate=config.autoencoder.learning_rate,
                    contamination=config.novelty.contamination,
                    seed=config.random_seed,
                ),
            ),
            ("normalize_embedding", Normalizer()),
        ])
