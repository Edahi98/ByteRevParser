UNKNOWN_LABEL = "nueva"


class DetectorCambiosService:
    """Compara una frase nueva contra el banco de frases de control de cambios aprendidas, usando un pipeline cargado en memoria.

    Singleton de una sola instancia por proceso. No lee ni escribe nada
    en disco: `load_artifacts()` recibe el pipeline ya deserializado (por
    ejemplo, a partir de un ZIP exportado por `/train_detector_cambios` y
    subido de vuelta por el cliente) y lo deja listo para `compare()`. La
    decisión de "mismo cambio o no" se basa en la distancia al vecino más
    cercano del banco de referencia guardado en el propio encoder
    (`reference_embeddings_`) contra su `similarity_threshold_`, ambos
    calculados durante el entrenamiento.
    """

    _instance: "DetectorCambiosService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.pipeline = None
        self._initialized = True

    def load_artifacts(self, pipeline) -> None:
        self.pipeline = pipeline

    def compare(self, phrase: str) -> dict:
        """Compara una frase contra el banco de frases de control de cambios aprendidas; dice si habla de lo mismo que alguna de ellas."""
        encoder = self.pipeline.named_steps["encoder"]
        embedding = self.pipeline.transform([phrase])
        distancia, indice_mas_cercano = encoder.nearest_reference(embedding)

        distancia = float(distancia[0])
        frase_mas_parecida = str(encoder.reference_phrases_[indice_mas_cercano[0]])
        es_conocida = distancia <= encoder.similarity_threshold_

        return {
            "es_conocida": bool(es_conocida),
            "distancia": distancia,
            "frase_mas_parecida": frase_mas_parecida,
        }
