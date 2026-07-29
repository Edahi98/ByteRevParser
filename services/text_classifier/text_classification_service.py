import numpy as np

from services.text_classifier.cluster_labeling_service import ClusterLabelingService

UNKNOWN_LABEL = "Sin clasificar"


class TextClassificationService:
    """Ubica frases en un grupo (cluster) usando un pipeline de agrupamiento y un detector de ruido cargados en memoria.

    Singleton de una sola instancia por proceso. No lee ni escribe nada en
    disco: `load_artifacts()` recibe ambos pipelines ya deserializados
    (por ejemplo, a partir de un ZIP exportado por `/train_text_classifier`
    y subido de vuelta por el cliente) y los deja listos para `classify()`.
    El detector de ruido combina dos señales independientes: IsolationForest
    (sklearn, entrenado sobre el embedding) y el error de reconstrucción del
    autoencoder (PyTorch) para esa misma frase — si cualquiera de las dos
    la marca como rara, se descarta, sin importar a qué grupo caiga más
    cerca.
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
        self.labeling_service = ClusterLabelingService()
        self._initialized = True

    def load_artifacts(self, pipeline, novelty_pipeline) -> None:
        self.pipeline = pipeline
        self.novelty_pipeline = novelty_pipeline

    def classify(self, phrase: str) -> dict:
        """Ubica una frase en su grupo más cercano; la marca como ruido si el detector de novedad la rechaza."""
        features = self.pipeline.named_steps["features"]
        embedder = features.named_steps["embedder"]

        rechazo_bosque = self.novelty_pipeline.predict([phrase])[0] == -1
        tfidf_normalizado = features[:2].transform([phrase])
        error_reconstruccion = embedder.reconstruction_error(tfidf_normalizado)[0]
        es_ruido = bool(rechazo_bosque or error_reconstruccion > embedder.error_umbral_)

        kmeans = self.pipeline.named_steps["cluster"]
        distancias = kmeans.transform(features.transform([phrase]))[0]
        indices_ordenados = np.argsort(distancias)
        cluster_id = int(indices_ordenados[0])
        confianza = self._margen_confianza(distancias, indices_ordenados)

        if es_ruido:
            return {"etiqueta": UNKNOWN_LABEL, "confianza": confianza, "terminos_clave": []}

        terminos_clave = self.labeling_service.top_terms(self.pipeline, cluster_id)
        return {"etiqueta": f"Grupo {cluster_id}", "confianza": confianza, "terminos_clave": terminos_clave}

    def _margen_confianza(self, distancias: np.ndarray, indices_ordenados: np.ndarray) -> float:
        distancia_mas_cercana = distancias[indices_ordenados[0]]
        if len(indices_ordenados) == 1:
            return 1.0

        distancia_segunda_mas_cercana = distancias[indices_ordenados[1]]
        if distancia_segunda_mas_cercana == 0:
            return 1.0

        return float((distancia_segunda_mas_cercana - distancia_mas_cercana) / distancia_segunda_mas_cercana)
