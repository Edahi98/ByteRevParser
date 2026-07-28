import zipfile
from io import BytesIO

TFIDF_SUFFIX = "_tfidf.joblib"
WORD2VEC_SUFFIX = "_word2vec.joblib"
REPORT_SUFFIX = "_reporte.json"


class ArtifactArchiveService:
    """Empaqueta y desempaqueta en un único ZIP los artefactos exportables del clasificador.

    Los nombres de las entradas se derivan del `model_name` recibido en
    `build()`, para que varios modelos entrenados por separado convivan
    como ZIPs y archivos internos claramente distinguibles. `extract()` no
    necesita conocer ese nombre: localiza cada entrada por su sufijo.
    """

    def build(
        self, model_name: str, model_bytes: bytes, tfidf_bytes: bytes, word2vec_bytes: bytes, report_bytes: bytes
    ) -> bytes:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr(f"{model_name}.joblib", model_bytes)
            archive.writestr(f"{model_name}{TFIDF_SUFFIX}", tfidf_bytes)
            archive.writestr(f"{model_name}{WORD2VEC_SUFFIX}", word2vec_bytes)
            archive.writestr(f"{model_name}{REPORT_SUFFIX}", report_bytes)
        return buffer.getvalue()

    def extract(self, archive_bytes: bytes) -> tuple[bytes, bytes, bytes]:
        with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
            names = archive.namelist()
            tfidf_entry = self._find_by_suffix(names, TFIDF_SUFFIX)
            word2vec_entry = self._find_by_suffix(names, WORD2VEC_SUFFIX)
            model_entry = self._find_model_entry(names, tfidf_entry, word2vec_entry)

            return archive.read(model_entry), archive.read(tfidf_entry), archive.read(word2vec_entry)

    def _find_by_suffix(self, names: list[str], suffix: str) -> str:
        for name in names:
            if name.endswith(suffix):
                return name
        raise ValueError(f"El ZIP de artefactos no contiene ningún archivo terminado en '{suffix}'.")

    def _find_model_entry(self, names: list[str], tfidf_entry: str, word2vec_entry: str) -> str:
        for name in names:
            if name.endswith(".joblib") and name not in (tfidf_entry, word2vec_entry):
                return name
        raise ValueError("El ZIP de artefactos no contiene el archivo del modelo principal (.joblib).")
