import zipfile
from io import BytesIO

MODEL_ENTRY = "modelo.joblib"
REPORT_ENTRY = "reporte.json"


class ArtifactArchiveService:
    """Empaqueta y desempaqueta en un ZIP el pipeline de detección de control de cambios y su reporte de entrenamiento."""

    def build(self, model_bytes: bytes, report_bytes: bytes) -> bytes:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(MODEL_ENTRY, model_bytes)
            archive.writestr(REPORT_ENTRY, report_bytes)
        return buffer.getvalue()

    def extract(self, archive_bytes: bytes) -> bytes:
        with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
            if MODEL_ENTRY not in archive.namelist():
                raise ValueError(f"El ZIP de artefactos no contiene '{MODEL_ENTRY}'.")
            return archive.read(MODEL_ENTRY)
