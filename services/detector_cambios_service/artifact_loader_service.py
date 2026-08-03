from services.detector_cambios_service.artifact_archive_service import ArtifactArchiveService
from services.detector_cambios_service.model_persistence_service import ModelPersistenceService


class ArtifactLoaderService:
    """Convierte el ZIP de artefactos del detector en su encoder ya deserializado.

    Une los dos pasos que siempre van juntos —sacar `modelo.joblib` del ZIP y
    deserializarlo— para que los callers no repitan la pareja. Propaga el
    `ValueError` de `ArtifactArchiveService` cuando el ZIP no trae el modelo.
    """

    def __init__(self):
        self.archive_service = ArtifactArchiveService()
        self.persistence_service = ModelPersistenceService()

    def load(self, archive_bytes: bytes):
        return self.persistence_service.load(self.archive_service.extract(archive_bytes))
