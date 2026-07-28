import polars as pl

from services.text_classifier.feature_service import FeatureService

REQUIRED_COLUMN = "frase"


class PredictorService:
    """Predice la clase de frases nuevas leídas desde un CSV con polars."""

    def predict_from_csv(self, csv_path: str, model, feature_service: FeatureService) -> list[dict]:
        df_nuevas = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df_nuevas.columns:
            raise ValueError(f"El CSV de frases nuevas debe tener una columna '{REQUIRED_COLUMN}'.")

        frases_nuevas = df_nuevas.get_column(REQUIRED_COLUMN).to_list()
        X_nuevas = feature_service.build(frases_nuevas)
        predicciones = model.predict(X_nuevas)

        return [
            {"frase": frase, "etiqueta": str(etiqueta)}
            for frase, etiqueta in zip(frases_nuevas, predicciones)
        ]
