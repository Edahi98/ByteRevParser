import gc
import os

import torch
from sentence_transformers import CrossEncoder

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "models_ai", "jina-reranker-v2-base-multilingual"
)


class CrossEncoderService:
    """Reordena una lista de candidatos por relevancia semántica frente a una query.

    Singleton de una sola instancia por proceso, pero el modelo
    (jina-reranker-v2-base-multilingual) ya no se mantiene cargado entre
    llamadas: `rerank()` lo carga bajo demanda y lo libera de memoria justo
    después de usarlo, para no mantener el footprint de RAM/VRAM alto todo el
    tiempo que vive el proceso.
    """

    _instance: "CrossEncoderService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.model: CrossEncoder | None = None
        self._initialized = True

    def _load(self) -> None:
        self.model = CrossEncoder(
            MODEL_PATH,
            automodel_args={"torch_dtype": "auto"},
            trust_remote_code=True,
        )

    def _unload(self) -> None:
        self.model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def rerank(self, query: str, candidates: list, top_k: int | None = None) -> list:
        if not candidates:
            return []

        self._load()
        try:
            pairs = [[query, str(candidate)] for candidate in candidates]
            scores = self.model.predict(pairs)
        finally:
            self._unload()

        ranked = sorted(zip(candidates, scores), key=lambda pair: pair[1], reverse=True)
        ranked_candidates = [candidate for candidate, _score in ranked]

        if top_k is not None:
            return ranked_candidates[:top_k]

        return ranked_candidates
