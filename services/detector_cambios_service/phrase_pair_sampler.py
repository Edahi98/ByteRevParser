import numpy as np


class PhrasePairSampler:
    """Arma pares (i, j, etiqueta) para entrenamiento contrastivo a partir de un origin_id por fila.

    Un par es positivo (etiqueta 1) si ambas filas comparten `origin_id`
    (son variantes de la misma frase original) y negativo (etiqueta 0) si
    vienen de orígenes distintos. Se llama una vez por época desde
    `DetectorCambiosEncoder.fit`, para que el modelo vea combinaciones
    distintas de pares en cada pasada en vez de siempre las mismas.

    Una fila sin compañeros (grupo de tamaño 1) solo puede venir de
    `HardNegativeService`: es una frase genuinamente ajena al dominio, no
    una variante de control de cambios. Sin tratamiento especial, un
    ancla real solo topa con una de esas frases ajenas por azar — con
    ~1,000 negativos externos sobre ~11,000 filas totales, eso es ~9% de
    sus negativos, demasiado poco para que la red aprenda una frontera
    real contra contenido ajeno (deep learning permisivo). Por eso, la
    mitad de los negativos de cada ancla real se reserva explícitamente
    para frases ajenas cuando existen, en vez de dejarlo al azar.
    """

    def build_pairs(self, origin_ids: np.ndarray, pairs_per_anchor: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        origin_ids = np.asarray(origin_ids)
        n_muestras = len(origin_ids)

        indices_por_origen: dict = {}
        for indice, origen in enumerate(origin_ids):
            indices_por_origen.setdefault(origen, []).append(indice)

        indices_ajenos = np.array(
            [indices[0] for indices in indices_por_origen.values() if len(indices) == 1]
        )

        anclas, pares, etiquetas = [], [], []
        for ancla in range(n_muestras):
            origen_ancla = origin_ids[ancla]
            companeros = indices_por_origen[origen_ancla]
            es_ancla_real = len(companeros) > 1

            if es_ancla_real:
                positivo = ancla
                while positivo == ancla:
                    positivo = companeros[rng.integers(len(companeros))]
                anclas.append(ancla)
                pares.append(positivo)
                etiquetas.append(1)

            n_negativos_ajenos = pairs_per_anchor // 2 if es_ancla_real and len(indices_ajenos) > 0 else 0
            for i in range(pairs_per_anchor):
                if i < n_negativos_ajenos:
                    negativo = indices_ajenos[rng.integers(len(indices_ajenos))]
                else:
                    negativo = rng.integers(n_muestras)
                    while origin_ids[negativo] == origen_ancla:
                        negativo = rng.integers(n_muestras)
                anclas.append(ancla)
                pares.append(negativo)
                etiquetas.append(0)

        return np.array(anclas), np.array(pares), np.array(etiquetas, dtype=np.float32)
