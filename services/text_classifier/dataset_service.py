import polars as pl

REQUIRED_COLUMN = "frase"


class DatasetService:
    """Carga y valida el dataset de texto sin etiquetar con polars."""

    def load_unlabeled(self, csv_path: str) -> pl.DataFrame:
        """Carga el CSV y valida que tenga la columna 'frase', sin nulos ni frases vacías."""
        df = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df.columns:
            raise ValueError(f"El CSV debe contener la columna '{REQUIRED_COLUMN}', encontradas: {set(df.columns)}")

        if df.select(pl.col(REQUIRED_COLUMN).is_null().any()).to_numpy().any():
            raise ValueError("El dataset contiene valores nulos en 'frase'.")

        df = df.with_columns(pl.col(REQUIRED_COLUMN).str.strip_chars().alias(REQUIRED_COLUMN))
        if (df.get_column(REQUIRED_COLUMN) == "").any():
            raise ValueError("El dataset contiene frases vacías.")

        return df
