import zipfile
from io import BytesIO

NOVELTY_SUFFIX = "_novedad.joblib"
REPORT_SUFFIX = "_reporte.json"
MODEL_SUFFIX = ".joblib"


class ArtifactArchiveService:
    """Empaqueta y desempaqueta en un ZIP el pipeline clasificador, el detector de novedad y el reporte.

    El nombre de las entradas se deriva del `model_name` recibido en
    `build()`, para que varios modelos entrenados por separado convivan
    como ZIPs claramente distinguibles. `extract()` no necesita conocer
    ese nombre: localiza cada entrada por su sufijo.
    """

    def build(self, model_name: str, model_bytes: bytes, novelty_bytes: bytes, report_bytes: bytes) -> bytes:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(f"{model_name}{MODEL_SUFFIX}", model_bytes)
            archive.writestr(f"{model_name}{NOVELTY_SUFFIX}", novelty_bytes)
            archive.writestr(f"{model_name}{REPORT_SUFFIX}", report_bytes)
        return buffer.getvalue()

    def extract(self, archive_bytes: bytes) -> tuple[bytes, bytes]:
        with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
            names = archive.namelist()
            novelty_entry = self._find_by_suffix(names, NOVELTY_SUFFIX)
            model_entry = self._find_model_entry(names, novelty_entry)

            return archive.read(model_entry), archive.read(novelty_entry)

    def _find_by_suffix(self, names: list[str], suffix: str) -> str:
        for name in names:
            if name.endswith(suffix):
                return name
        raise ValueError(f"El ZIP de artefactos no contiene ningún archivo terminado en '{suffix}'.")

    def _find_model_entry(self, names: list[str], novelty_entry: str) -> str:
        for name in names:
            if name.endswith(MODEL_SUFFIX) and name != novelty_entry:
                return name
        raise ValueError(f"El ZIP de artefactos no contiene el archivo del pipeline principal ('{MODEL_SUFFIX}').")
