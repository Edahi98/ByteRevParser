import numpy as np
from gensim.models import Word2Vec

from services.text_classifier.tokenizer_service import TokenizerService

VECTOR_SIZE = 100
WINDOW = 5
MIN_COUNT = 2
RANDOM_SEED = 42


class Word2VecService:
    """Entrena un Word2Vec propio (skip-gram) y vectoriza frases como promedio de tokens."""

    def __init__(self, tokenizer_service: TokenizerService):
        self.tokenizer_service = tokenizer_service
        self.model: Word2Vec | None = None

    def train(self, phrases: list[str]) -> None:
        corpus_tokenizado = [self.tokenizer_service.tokenize(frase) for frase in phrases]
        self.model = Word2Vec(
            sentences=corpus_tokenizado,
            sg=1,
            vector_size=VECTOR_SIZE,
            window=WINDOW,
            min_count=MIN_COUNT,
            seed=RANDOM_SEED,
        )

    def use_trained_model(self, word2vec_model: Word2Vec) -> None:
        """Sustituye el modelo interno por uno ya entrenado (p. ej. cargado desde disco)."""
        self.model = word2vec_model

    def vectorize_phrase(self, phrase: str) -> np.ndarray:
        """Promedia los vectores de los tokens presentes en el vocabulario.

        Devuelve un vector de ceros si ninguno de los tokens de la frase
        pertenece al vocabulario aprendido.
        """
        tokens_conocidos = [
            token for token in self.tokenizer_service.tokenize(phrase) if token in self.model.wv
        ]
        if not tokens_conocidos:
            return np.zeros(self.model.vector_size, dtype=np.float32)
        return np.mean([self.model.wv[token] for token in tokens_conocidos], axis=0)
