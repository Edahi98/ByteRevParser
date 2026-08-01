import gc
import os

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models_ai", "jina-embeddings-v3"
)

UMBRAL_ES_CAMBIO = 0.73


class DetectorCambiosEncoder:
    """Detecta si una frase habla de control de cambios: embeddings preentrenados (jina-embeddings-v3) + regresión logística.

    `jina-embeddings-v3` ya trae el conocimiento semántico del lenguaje
    aprendido en su preentrenamiento, así que aquí no se entrena ningún
    encoder desde cero — solo la regresión logística sobre esos
    embeddings. El modelo se carga bajo demanda y se libera justo
    después de usarse (igual que `RedactorService`/`NuExtractService`), porque pesa
    ~1.6GB y solo hace falta durante `fit`/`predict`. `es_cambio` exige
    `UMBRAL_ES_CAMBIO` (0.73) en vez del 0.5 por defecto de la regresión
    logística, para no marcar como cambio una frase donde el modelo
    apenas se inclina más hacia sí que hacia no (p. ej. un 55%).
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.classifier = LogisticRegression(random_state=seed, max_iter=1000)

    def fit(self, frases: list[str], etiquetas: list[int]) -> "DetectorCambiosEncoder":
        embeddings = self._encode(frases)
        self.classifier.fit(embeddings, etiquetas)
        return self

    def predict(self, frases: list[str]) -> tuple[np.ndarray, np.ndarray]:
        embeddings = self._encode(frases)
        probabilidad = self.classifier.predict_proba(embeddings)[:, 1]
        es_cambio = probabilidad >= UMBRAL_ES_CAMBIO
        return es_cambio, probabilidad

    def _encode(self, frases: list[str]) -> np.ndarray:
        embedder = SentenceTransformer(MODEL_PATH, trust_remote_code=True)
        try:
            return embedder.encode(frases, convert_to_numpy=True, show_progress_bar=False)
        finally:
            del embedder
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
