import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from services.text_classifier.spanish_stopwords_service import SpanishStopwordsService
from services.text_classifier.word2vec_service import Word2VecService

TFIDF_NGRAM_RANGE = (1, 3)
TFIDF_MAX_FEATURES = 5000


class FeatureService:
    """Construye la matriz de features híbrida: TF-IDF + Word2Vec normalizados y concatenados."""

    def __init__(self, word2vec_service: Word2VecService, stopwords_service: SpanishStopwordsService):
        self.word2vec_service = word2vec_service
        self.tfidf = TfidfVectorizer(
            ngram_range=TFIDF_NGRAM_RANGE,
            max_features=TFIDF_MAX_FEATURES,
            stop_words=stopwords_service.get(),
        )

    def fit(self, phrases: list[str]) -> None:
        self.tfidf.fit(phrases)

    def use_fitted_tfidf(self, tfidf: TfidfVectorizer) -> None:
        """Sustituye el TF-IDF interno por uno ya ajustado (p. ej. cargado desde disco)."""
        self.tfidf = tfidf

    def build(self, phrases: list[str]) -> np.ndarray:
        matriz_tfidf = normalize(self.tfidf.transform(phrases).toarray())
        matriz_w2v = normalize(
            np.vstack([self.word2vec_service.vectorize_phrase(frase) for frase in phrases])
        )
        return np.hstack([matriz_tfidf, matriz_w2v])
