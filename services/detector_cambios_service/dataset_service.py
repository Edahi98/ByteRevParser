import polars as pl


class DatasetService:
    """Carga el dataset de entrenamiento de control de cambios (frase + origin_id) con polars.

    El CSV lo genera siempre `data/generador_nlp/main.py` con ambas
    columnas garantizadas y sin valores nulos ni frases vacías — no hace
    falta revalidar aquí un archivo que este mismo proyecto produce.
    """

    def load(self, csv_path: str) -> pl.DataFrame:
        return pl.read_csv(csv_path)
