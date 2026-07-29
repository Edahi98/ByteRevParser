import numpy as np
import polars as pl

from services.text_classifier.cluster_labeling_service import ClusterLabelingService

REQUIRED_COLUMN = "frase"
UNKNOWN_LABEL = "Sin clasificar"


class PredictorService:
    """Ubica en lote frases nuevas leídas desde un CSV con polars en su grupo más cercano.

    Usa un pipeline de agrupamiento y un detector de ruido ya entrenados,
    igual que `TextClassificationService` pero de forma vectorizada. Los
    términos clave por cluster se calculan una sola vez por cluster
    presente en el lote, no por fila, para no repetir el mismo cálculo de
    `ClusterLabelingService` miles de veces en datasets grandes.
    """

    def __init__(self):
        self.labeling_service = ClusterLabelingService()

    def predict_from_csv(self, csv_path: str, pipeline, novelty_pipeline) -> list[dict]:
        df_nuevas = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df_nuevas.columns:
            raise ValueError(f"El CSV de frases nuevas debe tener una columna '{REQUIRED_COLUMN}'.")

        frases_nuevas = df_nuevas.get_column(REQUIRED_COLUMN).to_list()
        rechazo_bosque = novelty_pipeline.predict(frases_nuevas)

        features = pipeline.named_steps["features"]
        embedder = features.named_steps["embedder"]
        kmeans = pipeline.named_steps["cluster"]

        tfidf_normalizado = features[:2].transform(frases_nuevas)
        errores_reconstruccion = embedder.reconstruction_error(tfidf_normalizado)
        matriz_distancias = kmeans.transform(features.transform(frases_nuevas))

        cache_terminos: dict[int, list[str]] = {}
        predicciones = []
        for frase, distancias_frase, rechazo, error_reconstruccion in zip(
            frases_nuevas, matriz_distancias, rechazo_bosque, errores_reconstruccion
        ):
            indices_ordenados = np.argsort(distancias_frase)
            cluster_id = int(indices_ordenados[0])
            confianza = self._margen_confianza(distancias_frase, indices_ordenados)
            es_ruido = rechazo == -1 or error_reconstruccion > embedder.error_umbral_

            if es_ruido:
                predicciones.append(
                    {"frase": frase, "etiqueta": UNKNOWN_LABEL, "confianza": confianza, "terminos_clave": []}
                )
                continue

            if cluster_id not in cache_terminos:
                cache_terminos[cluster_id] = self.labeling_service.top_terms(pipeline, cluster_id)

            predicciones.append(
                {
                    "frase": frase,
                    "etiqueta": f"Grupo {cluster_id}",
                    "confianza": confianza,
                    "terminos_clave": cache_terminos[cluster_id],
                }
            )

        return predicciones

    def _margen_confianza(self, distancias: np.ndarray, indices_ordenados: np.ndarray) -> float:
        distancia_mas_cercana = distancias[indices_ordenados[0]]
        if len(indices_ordenados) == 1:
            return 1.0

        distancia_segunda_mas_cercana = distancias[indices_ordenados[1]]
        if distancia_segunda_mas_cercana == 0:
            return 1.0

        return float((distancia_segunda_mas_cercana - distancia_mas_cercana) / distancia_segunda_mas_cercana)
