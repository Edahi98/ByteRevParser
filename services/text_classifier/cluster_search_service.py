import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from models.text_classifier_config import TextClassifierConfig


class ClusterSearchService:
    """Busca el mejor número de grupos (K) para KMeans probando un rango y comparando por silhouette score.

    Igual que antes se elegía el mejor de varios clasificadores por
    F1-macro, aquí se prueba cada K en `TextClassifierConfig.clustering`
    y se conserva el que mejor separa los grupos. `k_max` se recorta a
    `n_samples - 1` porque silhouette_score exige al menos 2 grupos y
    menos grupos que muestras.
    """

    def search(self, X: np.ndarray, config: TextClassifierConfig) -> dict:
        n_samples = X.shape[0]
        k_min = max(2, config.clustering.k_min)
        k_max = max(k_min, min(config.clustering.k_max, n_samples - 1))

        silhouette_por_k = {}
        mejor_k = None
        mejor_modelo = None
        mejor_puntaje = -1.0

        for k in range(k_min, k_max + 1):
            modelo = KMeans(n_clusters=k, random_state=config.random_seed, n_init=10)
            etiquetas = modelo.fit_predict(X)
            puntaje = float(silhouette_score(X, etiquetas))
            silhouette_por_k[k] = puntaje

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_k = k
                mejor_modelo = modelo

        return {"mejor_k": mejor_k, "mejor_modelo": mejor_modelo, "silhouette_por_k": silhouette_por_k}
