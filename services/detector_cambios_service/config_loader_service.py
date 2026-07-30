import json
import os

from models.detector_cambios_config import DetectorCambiosConfig

CONFIG_PATH = os.path.join("config", "detector_cambios_config.json")


class ConfigLoaderService:
    """Carga la configuración del detector de control de cambios desde su JSON fijo."""

    def load(self) -> DetectorCambiosConfig:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return DetectorCambiosConfig(**data)
