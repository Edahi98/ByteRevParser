from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import Normalizer

from models.text_classifier_config import TextClassifierConfig
from services.text_classifier.spanish_stopwords_service import SpanishStopwordsService
from services.text_classifier.word2vec_vectorizer import Word2VecVectorizer


class FeaturePipelineFactory:
    """Construye el FeatureUnion de TF-IDF + Word2Vec (normalizados por separado) como un solo transformer.

    Un `staticmethod` en vez de una función suelta, siguiendo el mismo
    patrón de fábrica que `BinaryAdapterFactory`. Los hiperparámetros
    vienen de `TextClassifierConfig`, no están fijos en el código.
    """

    @staticmethod
    def create(config: TextClassifierConfig) -> FeatureUnion:
        return FeatureUnion([
            (
                "tfidf",
                Pipeline([
                    (
                        "vectorizer",
                        TfidfVectorizer(
                            ngram_range=config.tfidf.ngram_range,
                            max_features=config.tfidf.max_features,
                            stop_words=SpanishStopwordsService().get(),
                        ),
                    ),
                    ("normalize", Normalizer()),
                ]),
            ),
            (
                "word2vec",
                Pipeline([
                    (
                        "vectorizer",
                        Word2VecVectorizer(
                            vector_size=config.word2vec.vector_size,
                            window=config.word2vec.window,
                            min_count=config.word2vec.min_count,
                            sg=config.word2vec.sg,
                            seed=config.random_seed,
                        ),
                    ),
                    ("normalize", Normalizer()),
                ]),
            ),
        ])
