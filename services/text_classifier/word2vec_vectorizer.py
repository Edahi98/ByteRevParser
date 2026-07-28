import numpy as np
from gensim.models import Word2Vec
from sklearn.base import BaseEstimator, TransformerMixin

from services.text_classifier.tokenizer_service import TokenizerService


class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    """Transformer de scikit-learn: entrena un Word2Vec propio y vectoriza frases como promedio de tokens.

    Vector de frase = promedio de los vectores de los tokens presentes en
    el vocabulario aprendido; vector de ceros si ninguno existe. Al ser un
    TransformerMixin de scikit-learn, encaja directamente en un Pipeline
    o FeatureUnion junto con TfidfVectorizer.
    """

    def __init__(self, vector_size: int = 100, window: int = 5, min_count: int = 2, sg: int = 1, seed: int = 42):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.sg = sg
        self.seed = seed

    def fit(self, X, y=None):
        tokenizer_service = TokenizerService()
        corpus_tokenizado = [tokenizer_service.tokenize(frase) for frase in X]
        self.model_ = Word2Vec(
            sentences=corpus_tokenizado,
            sg=self.sg,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            seed=self.seed,
        )
        return self

    def transform(self, X) -> np.ndarray:
        tokenizer_service = TokenizerService()
        return np.vstack([self._vectorize_phrase(frase, tokenizer_service) for frase in X])

    def _vectorize_phrase(self, phrase: str, tokenizer_service: TokenizerService) -> np.ndarray:
        tokens_conocidos = [token for token in tokenizer_service.tokenize(phrase) if token in self.model_.wv]
        if not tokens_conocidos:
            return np.zeros(self.vector_size, dtype=np.float32)
        return np.mean([self.model_.wv[token] for token in tokens_conocidos], axis=0)
