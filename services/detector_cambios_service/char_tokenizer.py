import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

PAD_TOKEN = 0
UNK_TOKEN = 1


class CharTokenizer(BaseEstimator, TransformerMixin):
    """Convierte frases en secuencias de índices de caracteres para un encoder profundo entrenado desde cero.

    A diferencia de TF-IDF (una bolsa de fragmentos ya fija antes de
    entrenar), esto deja que la propia red aprenda cómo combinar los
    caracteres — el orden y el contexto de la frase importan, no solo
    qué fragmentos aparecen. El vocabulario de caracteres se construye
    sobre las frases de entrenamiento (`fit`); cualquier carácter nuevo
    en inferencia cae en el token "desconocido" reservado (`UNK_TOKEN`).
    El índice 0 queda reservado para relleno (`PAD_TOKEN`), para que el
    encoder pueda distinguir posiciones reales de relleno.
    """

    def __init__(self, max_length: int = 160, lowercase: bool = True):
        self.max_length = max_length
        self.lowercase = lowercase

    def fit(self, X, y=None):
        textos = [t.lower() if self.lowercase else t for t in X]
        caracteres = sorted(set("".join(textos)))
        self.char_to_index_ = {caracter: indice + 2 for indice, caracter in enumerate(caracteres)}
        self.vocab_size_ = len(self.char_to_index_) + 2
        return self

    def transform(self, X) -> np.ndarray:
        textos = [t.lower() if self.lowercase else t for t in X]
        secuencias = np.full((len(textos), self.max_length), PAD_TOKEN, dtype=np.int64)

        for fila, texto in enumerate(textos):
            for columna, caracter in enumerate(texto[: self.max_length]):
                secuencias[fila, columna] = self.char_to_index_.get(caracter, UNK_TOKEN)

        return secuencias
