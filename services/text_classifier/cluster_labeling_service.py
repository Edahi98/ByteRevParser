import numpy as np
from sklearn.pipeline import Pipeline


class ClusterLabelingService:
    """Calcula los fragmentos de texto más representativos de un cluster, a partir de su centroide.

    El centroide vive en el espacio reducido por el autoencoder; se
    proyecta de vuelta al espacio TF-IDF pasándolo por el decoder
    (`embedder.inverse_transform`) y se toman los pesos más altos. Como
    el TF-IDF usa `analyzer='char_wb'` (para tolerar errores
    ortográficos), los "términos" resultantes son n-gramas de caracteres
    (p. ej. "cam", "bio ") y no siempre palabras completas, pero igual
    sirven como pista de qué distingue a cada grupo.
    """

    def top_terms(self, cluster_pipeline: Pipeline, cluster_id: int, n_terms: int = 5) -> list[str]:
        features = cluster_pipeline.named_steps["features"]
        vectorizer = features.named_steps["vectorizer"]
        embedder = features.named_steps["embedder"]
        kmeans = cluster_pipeline.named_steps["cluster"]

        centroide = kmeans.cluster_centers_[cluster_id].reshape(1, -1)
        espacio_tfidf = embedder.inverse_transform(centroide)[0]
        terminos = vectorizer.get_feature_names_out()

        candidatos_por_peso = np.argsort(espacio_tfidf)[::-1]

        terminos_unicos = []
        for indice in candidatos_por_peso:
            termino = str(terminos[indice]).strip()
            if termino and termino not in terminos_unicos:
                terminos_unicos.append(termino)
            if len(terminos_unicos) == n_terms:
                break

        return terminos_unicos

    def representative_phrases(
        self, frases: list[str], X: np.ndarray, kmeans, cluster_id: int, n_ejemplos: int = 5
    ) -> list[str]:
        """Devuelve las frases de entrenamiento más cercanas al centroide de un cluster.

        A diferencia de `top_terms` (fragmentos de caracteres, útiles pero
        difíciles de leer), estas son frases reales del dataset: la forma
        más confiable de que una persona entienda qué representa cada
        grupo. Solo puede calcularse en tiempo de entrenamiento, porque
        necesita las frases y su matriz de features originales (el
        pipeline ya exportado no las conserva).
        """
        indices_cluster = np.where(kmeans.labels_ == cluster_id)[0]
        centroide = kmeans.cluster_centers_[cluster_id]

        distancias = np.linalg.norm(X[indices_cluster] - centroide, axis=1)
        orden = np.argsort(distancias)[:n_ejemplos]

        return [frases[indices_cluster[i]] for i in orden]
