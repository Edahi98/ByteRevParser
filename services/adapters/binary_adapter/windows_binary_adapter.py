from services.adapters.binary_adapter.base import BinaryAdapter


class WindowsBinaryAdapter(BinaryAdapter):
    """Binarios `.exe` nativos de Windows."""

    _FILENAMES = {
        "tsubasa": "tsubasa.exe",
        "xmljava": "xmljava.exe",
    }

    def invocation_args(self, name: str, *args: str) -> list[str]:
        return [self.resolve(name), *args]
