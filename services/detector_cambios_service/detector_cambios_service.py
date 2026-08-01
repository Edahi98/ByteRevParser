class DetectorCambiosService:
    """Compara una frase nueva contra el detector de control de cambios entrenado, usando un encoder cargado en memoria.

    Singleton de una sola instancia por proceso. No lee ni escribe nada
    en disco: `load_artifacts()` recibe el `DetectorCambiosEncoder` ya
    deserializado (por ejemplo, a partir de un ZIP exportado por
    `/train_detector_cambios` y subido de vuelta por el cliente) y lo
    deja listo para `compare()`.
    """

    _instance: "DetectorCambiosService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.encoder = None
        self._initialized = True

    def load_artifacts(self, encoder) -> None:
        self.encoder = encoder

    def compare(self, phrase: str) -> dict:
        """Compara una frase contra el detector entrenado; dice si es control de cambios y con qué probabilidad."""
        es_cambio, probabilidad = self.encoder.predict([phrase])
        return {"es_cambio": bool(es_cambio[0]), "probabilidad": float(probabilidad[0])}
