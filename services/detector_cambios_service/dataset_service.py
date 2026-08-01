import os

import polars as pl

CAMBIOS_PATH = os.path.join("datasets", "datos_cambios.csv")
CALIDAD_PATH = os.path.join("datasets", "datos_calidad.csv")


class DatasetService:
    """Carga las frases de entrenamiento del detector de control de cambios como dos listas paralelas frase/etiqueta.

    `datasets/datos_cambios.csv` son frases reales de control de cambios
    (etiqueta 1) y `datasets/datos_calidad.csv` son frases ajenas al
    dominio (etiqueta 0) — clasificación binaria simple sobre embeddings
    preentrenados, sin necesidad de vincular cada frase con ninguna
    original.
    """

    def load(self) -> tuple[list[str], list[int]]:
        frases_cambios = pl.read_csv(CAMBIOS_PATH).get_column("frase").to_list()
        frases_calidad = pl.read_csv(CALIDAD_PATH).get_column("frase").to_list()

        frases = frases_cambios + frases_calidad
        etiquetas = [1] * len(frases_cambios) + [0] * len(frases_calidad)
        return frases, etiquetas
