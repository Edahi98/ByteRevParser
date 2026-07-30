import io

import joblib


class ModelPersistenceService:
    """Serializa y deserializa un pipeline entrenado con joblib, en memoria.

    No escribe nada a disco: el caller decide qué hacer con los bytes
    resultantes (por ejemplo, empaquetarlos para exportarlos como descarga).
    """

    def dump(self, artifact) -> bytes:
        buffer = io.BytesIO()
        joblib.dump(artifact, buffer)
        return buffer.getvalue()

    def load(self, data: bytes):
        return joblib.load(io.BytesIO(data))
