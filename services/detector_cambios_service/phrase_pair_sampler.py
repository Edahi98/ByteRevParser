import numpy as np


class PhrasePairSampler:
    """Arma pares (i, j, etiqueta) para entrenamiento contrastivo a partir de un origin_id por fila.

    Un par es positivo (etiqueta 1) si ambas filas comparten `origin_id`
    (son variantes de la misma frase original) y negativo (etiqueta 0) si
    vienen de orígenes distintos. Se llama una vez por época desde
    `DetectorCambiosEncoder.fit`, para que el modelo vea combinaciones
    distintas de pares en cada pasada en vez de siempre las mismas.
    """

    def build_pairs(self, origin_ids: np.ndarray, pairs_per_anchor: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        origin_ids = np.asarray(origin_ids)
        n_muestras = len(origin_ids)

        indices_por_origen: dict = {}
        for indice, origen in enumerate(origin_ids):
            indices_por_origen.setdefault(origen, []).append(indice)

        anclas, pares, etiquetas = [], [], []
        for ancla in range(n_muestras):
            origen_ancla = origin_ids[ancla]
            companeros = indices_por_origen[origen_ancla]

            if len(companeros) > 1:
                positivo = ancla
                while positivo == ancla:
                    positivo = companeros[rng.integers(len(companeros))]
                anclas.append(ancla)
                pares.append(positivo)
                etiquetas.append(1)

            for _ in range(pairs_per_anchor):
                negativo = rng.integers(n_muestras)
                while origin_ids[negativo] == origen_ancla:
                    negativo = rng.integers(n_muestras)
                anclas.append(ancla)
                pares.append(negativo)
                etiquetas.append(0)

        return np.array(anclas), np.array(pares), np.array(etiquetas, dtype=np.float32)
