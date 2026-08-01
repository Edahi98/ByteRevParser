import polars as pl

REQUIRED_COLUMN = "frase"


class DetectorCambiosBatchService:
    """Compara en lote frases nuevas leídas desde un CSV con polars contra el detector de control de cambios entrenado."""

    def compare_from_csv(self, csv_path: str, encoder) -> list[dict]:
        df_nuevas = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df_nuevas.columns:
            raise ValueError(f"El CSV de frases nuevas debe tener una columna '{REQUIRED_COLUMN}'.")

        frases_nuevas = df_nuevas.get_column(REQUIRED_COLUMN).to_list()
        es_cambio, probabilidad = encoder.predict(frases_nuevas)

        return [
            {"frase": frase, "es_cambio": bool(es), "probabilidad": float(prob)}
            for frase, es, prob in zip(frases_nuevas, es_cambio, probabilidad)
        ]
