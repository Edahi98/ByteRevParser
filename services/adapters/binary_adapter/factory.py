import platform

from services.adapters.binary_adapter.base import BinaryAdapter
from services.adapters.binary_adapter.linux_binary_adapter import LinuxBinaryAdapter
from services.adapters.binary_adapter.windows_binary_adapter import WindowsBinaryAdapter


class BinaryAdapterFactory:
    """Selecciona el BinaryAdapter correcto para el sistema operativo actual."""

    @staticmethod
    def create() -> BinaryAdapter:
        system = platform.system()

        if system == "Windows":
            return WindowsBinaryAdapter()

        return LinuxBinaryAdapter()
