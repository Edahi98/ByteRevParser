import polars as pl

from services.text_classifier.config_loader_service import ConfigLoaderService

REQUIRED_COLUMN = "frase"
UNKNOWN_LABEL = "Sin clasificar"


class PredictorService:
    """Predice la clase de frases nuevas leídas desde un CSV con polars.

    Usa un pipeline clasificador y un detector de novedad ya entrenados;
    el detector actúa como filtro de ruido antes del clasificador. Los
    umbrales de confianza vienen de `TextClassifierConfig`.
    """

    def __init__(self):
        self.config = ConfigLoaderService().load()

    def predict_from_csv(self, csv_path: str, pipeline, novelty_pipeline) -> list[dict]:
        df_nuevas = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df_nuevas.columns:
            raise ValueError(f"El CSV de frases nuevas debe tener una columna '{REQUIRED_COLUMN}'.")

        frases_nuevas = df_nuevas.get_column(REQUIRED_COLUMN).to_list()
        es_ruido = novelty_pipeline.predict(frases_nuevas)
        probabilidades = pipeline.predict_proba(frases_nuevas)

        predicciones = []
        for frase, probs_frase, ruido in zip(frases_nuevas, probabilidades, es_ruido):
            indice_max = probs_frase.argmax()
            confianza = float(probs_frase[indice_max])

            if confianza >= self.config.classification.high_confidence_override:
                etiqueta = str(pipeline.classes_[indice_max])
            elif ruido == -1 or confianza < self.config.classification.confidence_threshold:
                etiqueta = UNKNOWN_LABEL
            else:
                etiqueta = str(pipeline.classes_[indice_max])

            predicciones.append({"frase": frase, "etiqueta": etiqueta, "confianza": confianza})

        return predicciones
