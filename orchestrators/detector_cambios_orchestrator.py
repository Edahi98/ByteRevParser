import numpy as np
from sklearn.model_selection import train_test_split

from models.detector_cambios_config import DetectorCambiosConfig
from services.detector_cambios_service.config_loader_service import ConfigLoaderService
from services.detector_cambios_service.dataset_service import DatasetService
from services.detector_cambios_service.detector_cambios_encoder import DetectorCambiosEncoder


class DetectorCambiosOrchestrator:
    """Orquesta el entrenamiento del detector de control de cambios: dataset -> embeddings preentrenados -> regresión logística.

    Aparta un 20% de las frases como prueba antes de entrenar, para
    reportar una precisión honesta sobre datos que el clasificador nunca
    vio, en vez de medir contra las mismas frases con las que se ajustó.
    """

    def __init__(self):
        self.dataset_service = DatasetService()
        self.config = ConfigLoaderService().load()

    def run(self, config: DetectorCambiosConfig | None = None) -> dict:
        config = config or self.config

        frases, etiquetas = self.dataset_service.load()
        frases_train, frases_test, etiquetas_train, etiquetas_test = train_test_split(
            frases, etiquetas, test_size=0.2, random_state=config.random_seed
        )

        encoder = DetectorCambiosEncoder(seed=config.random_seed)
        encoder.fit(frases_train, etiquetas_train)

        es_cambio_test, _ = encoder.predict(frases_test)
        precision = float((es_cambio_test == np.array(etiquetas_test, dtype=bool)).mean())

        report = {
            "n_frases_entrenamiento": len(frases_train),
            "n_frases_prueba": len(frases_test),
            "precision": precision,
            "configuracion_usada": config.model_dump(),
        }

        return {"model": encoder, "report": report}
