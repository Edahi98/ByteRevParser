import json
import os

from models.text_classifier_config import TextClassifierConfig

DEFAULT_CONFIG_PATH = os.path.join("config", "text_classifier_config.json")


class ConfigLoaderService:
    """Carga la configuración del clasificador de texto desde un JSON, con valores por defecto.

    Si el archivo no existe, usa los valores por defecto de
    `TextClassifierConfig`, para que el clasificador siga funcionando sin
    exigir un archivo de configuración presente.
    """

    def load(self, config_path: str = DEFAULT_CONFIG_PATH) -> TextClassifierConfig:
        if not os.path.exists(config_path):
            return TextClassifierConfig()

        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return TextClassifierConfig(**data)
