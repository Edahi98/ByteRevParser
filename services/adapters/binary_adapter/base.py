import os
from abc import ABC, abstractmethod

RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "resources")


class BinaryAdapter(ABC):
    """Adapta el nombre lógico de un binario externo (`tsubasa`, `xmljava`) a la
    ruta del artefacto correcto para el sistema operativo actual, para que
    `TsubasaService` y `XmlJavaService` no necesiten conocer la extensión ni el
    layout de `resources/` de cada plataforma."""

    _FILENAMES: dict[str, str] = {}

    def resolve(self, name: str) -> str:
        try:
            filename = self._FILENAMES[name]
        except KeyError:
            raise ValueError(f"Unknown binary name for {type(self).__name__}: {name}") from None

        return os.path.join(RESOURCES_DIR, filename)

    @abstractmethod
    def invocation_args(self, name: str, *args: str) -> list[str]:
        """Arma el argv completo para invocar el binario `name` con `args`."""
