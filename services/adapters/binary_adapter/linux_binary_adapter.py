from services.adapters.binary_adapter.base import BinaryAdapter


class LinuxBinaryAdapter(BinaryAdapter):
    """Binarios ELF de Linux, ejecutables solo dentro de Docker o WSL."""

    _FILENAMES = {
        "tsubasa": "tsubasa",
        "xmljava": "xmljava-docker",
    }

    def invocation_args(self, name: str, *args: str) -> list[str]:
        return [self.resolve(name), *args]
