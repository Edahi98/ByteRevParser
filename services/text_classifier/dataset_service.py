import polars as pl

REQUIRED_COLUMNS = {"frase", "etiqueta"}


class DatasetService:
    """Carga y valida el dataset de texto etiquetado con polars."""

    def load_labeled(self, csv_path: str) -> pl.DataFrame:
        """Carga el CSV etiquetado y valida que tenga las columnas requeridas, sin nulos ni frases vacías."""
        df = pl.read_csv(csv_path)

        if not REQUIRED_COLUMNS.issubset(set(df.columns)):
            raise ValueError(
                f"El CSV debe contener las columnas {REQUIRED_COLUMNS}, "
                f"encontradas: {set(df.columns)}"
            )

        if df.select(pl.col("frase", "etiqueta").is_null().any()).to_numpy().any():
            raise ValueError("El dataset contiene valores nulos en 'frase' o 'etiqueta'.")

        df = df.with_columns(pl.col("frase").str.strip_chars().alias("frase"))
        if (df.get_column("frase") == "").any():
            raise ValueError("El dataset contiene frases vacías.")

        return df

    def class_distribution(self, df: pl.DataFrame) -> list[dict]:
        """Cuenta los ejemplos por clase, ordenados alfabéticamente por etiqueta."""
        conteo_por_clase = df.group_by("etiqueta").agg(pl.len().alias("conteo")).sort("etiqueta")
        return conteo_por_clase.to_dicts()
