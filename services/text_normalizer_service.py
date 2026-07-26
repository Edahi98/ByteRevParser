import unicodedata


class TextNormalizerService:
    """Elimina diacríticos (tildes, ñ) de un texto.

    RedactorService y NuExtractService cargan modelos .gguf cuya tabla de
    vocabulario corrompe caracteres UTF-8 multibyte (tildes, ñ) tanto al
    tokenizar la entrada como al generar texto. Mientras se usen esos
    archivos, normalizar a ASCII antes/después de pasarlos por el modelo
    evita esa corrupción a costa de perder el diacrítico original.
    """

    @staticmethod
    def strip_accents(text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(char for char in normalized if not unicodedata.combining(char))
