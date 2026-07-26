import os
import subprocess

from services.adapters.binary_adapter import BinaryAdapterFactory


class XmlJavaService:
    """Ejecuta el binario xmljava (Linux: resources/xmljava-docker, Windows: resources/xmljava.exe)
    para convertir un archivo de entrada a XML."""

    def __init__(self) -> None:
        self._binary_adapter = BinaryAdapterFactory.create()

    def convert(self, input_path: str, output_path: str | None = None) -> str:
        binary_path = self._binary_adapter.resolve("xmljava")
        if not os.path.exists(binary_path):
            raise FileNotFoundError(f"xmljava binary not found: {binary_path}")

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if output_path is None:
            output_path = os.path.splitext(input_path)[0] + ".xml"

        argv = self._binary_adapter.invocation_args("xmljava", input_path, output_path)
        result = subprocess.run(
            argv,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"xmljava failed: {result.stderr.strip()}")

        return output_path
