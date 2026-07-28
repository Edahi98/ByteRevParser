import string


class TokenizerService:
    """Tokeniza frases en palabras normalizadas (minúsculas, sin puntuación)."""

    def __init__(self):
        self._translation_table = str.maketrans("", "", string.punctuation)

    def tokenize(self, phrase: str) -> list[str]:
        return phrase.lower().translate(self._translation_table).split()
