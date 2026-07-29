import numpy as np
from sklearn.pipeline import Pipeline

from models.text_classifier_config import TextClassifierConfig
from services.text_classifier.cluster_labeling_service import ClusterLabelingService
from services.text_classifier.cluster_search_service import ClusterSearchService
from services.text_classifier.config_loader_service import ConfigLoaderService
from services.text_classifier.dataset_service import DatasetService
from services.text_classifier.feature_pipeline_factory import FeaturePipelineFactory
from services.text_classifier.isolation_forest_factory import IsolationForestFactory


class TextClassifierOrchestrator:
    """Orquesta el entrenamiento completo: dataset -> features -> agrupamiento -> detector de ruido.

    No necesita etiquetas: los grupos se descubren solos con KMeans, sobre
    un único pipeline de features (TF-IDF de n-gramas de caracteres +
    autoencoder de PyTorch) que se ajusta una sola vez y se reutiliza
    tanto para el pipeline de agrupamiento como para el detector de
    ruido, evitando reentrenar la parte más cara dos veces. No persiste
    nada en disco: devuelve ambos
    pipelines junto con el reporte, para que el caller decida cómo
    exportarlos (p. ej. un ZIP descargable). `run()` recibe opcionalmente
    la configuración a usar (por ejemplo, combinando los valores del
    archivo con ajustes que el usuario cambió en el frontend); si no se
    pasa ninguna, usa la cargada por defecto de
    `config/text_classifier_config.json`, para que el mismo clasificador
    sirva para otros datasets sin tocar Python.
    """

    def __init__(self):
        self.dataset_service = DatasetService()
        self.cluster_search_service = ClusterSearchService()
        self.labeling_service = ClusterLabelingService()
        self.config = ConfigLoaderService().load()

    def run(self, csv_path: str, config: TextClassifierConfig | None = None) -> dict:
        config = config or self.config

        df = self.dataset_service.load_unlabeled(csv_path)
        frases = df.get_column("frase").to_list()

        features = FeaturePipelineFactory.create(config)
        X = features.fit_transform(frases)

        resultado_busqueda = self.cluster_search_service.search(X, config)
        kmeans = resultado_busqueda["mejor_modelo"]

        detector_ruido = IsolationForestFactory.create(config)
        detector_ruido.fit(X)

        pipeline_cluster = Pipeline([("features", features), ("cluster", kmeans)])
        pipeline_novedad = Pipeline([("features", features), ("detector", detector_ruido)])

        report = self._build_report(pipeline_cluster, kmeans, detector_ruido, X, frases, resultado_busqueda, config)

        return {"model": pipeline_cluster, "novelty_model": pipeline_novedad, "report": report}

    def _build_report(
        self,
        pipeline_cluster: Pipeline,
        kmeans,
        detector_ruido,
        X: np.ndarray,
        frases: list[str],
        resultado_busqueda: dict,
        config: TextClassifierConfig,
    ) -> dict:
        ids_cluster, tamanos = np.unique(kmeans.labels_, return_counts=True)
        clusters = [
            {
                "cluster_id": int(cluster_id),
                "tamano": int(tamano),
                "terminos_clave": self.labeling_service.top_terms(pipeline_cluster, int(cluster_id)),
                "ejemplos": self.labeling_service.representative_phrases(frases, X, kmeans, int(cluster_id)),
            }
            for cluster_id, tamano in zip(ids_cluster, tamanos)
        ]

        embedder = pipeline_cluster.named_steps["features"].named_steps["embedder"]
        rechazo_bosque = detector_ruido.predict(X) == -1
        rechazo_autoencoder = embedder.reconstruction_errors_ > embedder.error_umbral_

        return {
            "k_elegido": resultado_busqueda["mejor_k"],
            "silhouette_por_k": resultado_busqueda["silhouette_por_k"],
            "clusters": clusters,
            "frases_ruido": int(np.sum(rechazo_bosque | rechazo_autoencoder)),
            "configuracion_usada": config.model_dump(),
        }
