from services.text_classifier.config_loader_service import ConfigLoaderService

UNKNOWN_LABEL = "Sin clasificar"


class TextClassificationService:
    """Clasifica frases usando un pipeline clasificador y un detector de novedad cargados en memoria.

    Singleton de una sola instancia por proceso. No lee ni escribe nada en
    disco: `load_artifacts()` recibe ambos pipelines ya deserializados
    (por ejemplo, a partir de un ZIP exportado por `/train_text_classifier`
    y subido de vuelta por el cliente) y los deja listos para `classify()`.
    El detector de novedad actúa como filtro de ruido antes del
    clasificador: si una frase no se parece a nada visto en
    entrenamiento, se marca como ruido. Excepción: si el clasificador
    está muy seguro (>= classification.high_confidence_override en la
    config) se confía en él y se ignora el veto del detector de novedad,
    porque con pocos ejemplos de entrenamiento el detector puede
    rechazar frases válidas que el clasificador sí reconoce con
    confianza.
    """

    _instance: "TextClassificationService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.pipeline = None
        self.novelty_pipeline = None
        self.config = ConfigLoaderService().load()
        self._initialized = True

    def load_artifacts(self, pipeline, novelty_pipeline) -> None:
        self.pipeline = pipeline
        self.novelty_pipeline = novelty_pipeline

    def classify(self, phrase: str) -> dict:
        """Clasifica una frase; la marca como ruido si el detector de novedad la rechaza o la confianza es baja."""
        es_ruido = self.novelty_pipeline.predict([phrase])[0] == -1

        probabilidades = self.pipeline.predict_proba([phrase])[0]
        indice_max = probabilidades.argmax()
        confianza = float(probabilidades[indice_max])

        if confianza >= self.config.classification.high_confidence_override:
            etiqueta = str(self.pipeline.classes_[indice_max])
        elif es_ruido or confianza < self.config.classification.confidence_threshold:
            etiqueta = UNKNOWN_LABEL
        else:
            etiqueta = str(self.pipeline.classes_[indice_max])

        return {"etiqueta": etiqueta, "confianza": confianza}
