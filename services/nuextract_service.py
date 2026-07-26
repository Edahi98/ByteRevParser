import gc
import json
import os

from llama_cpp import Llama

from services.text_normalizer_service import TextNormalizerService

MODELS_AI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_ai")
GGUF_PATH = os.path.join(MODELS_AI_DIR, "NuExtract-1.5-tiny.Q8_0.gguf")


class NuExtractService:
    """Extrae datos estructurados de un texto siguiendo un esquema JSON (numind/NuExtract-1.5-tiny).

    Singleton de una sola instancia por proceso, pero el modelo ya no se mantiene
    cargado entre llamadas: `extract()` lo carga bajo demanda vía llama.cpp
    (`llama_cpp.Llama`) y lo libera de memoria justo después de usarlo.

    El vocabulario de este .gguf corrompe tildes y la `ñ` al tokenizar (se
    reproduce igual con `transformers` y con llama.cpp nativo, así que es un
    problema del propio archivo, no del loader). Mientras se use este .gguf,
    `TextNormalizerService.strip_accents` limpia la entrada y la salida del
    modelo para evitar esa corrupción, a costa de perder el diacrítico original.
    """

    _instance: "NuExtractService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.llm: Llama | None = None
        self._initialized = True

    def _load(self) -> None:
        self.llm = Llama(model_path=GGUF_PATH, n_ctx=4096, verbose=False)

    def _unload(self) -> None:
        self.llm = None
        gc.collect()

    def extract(self, text: str, schema: dict) -> dict:
        self._load()
        try:
            schema_str = json.dumps(schema, indent=4)
            clean_text = TextNormalizerService.strip_accents(text)
            prompt = f"<|input|>\n### Template:\n{schema_str}\n### Text:\n{clean_text}\n<|output|>\n"

            response = self.llm(prompt, max_tokens=1024, temperature=0, stop=["<|end-output|>"])
            output = TextNormalizerService.strip_accents(response["choices"][0]["text"])
        finally:
            self._unload()

        return json.loads(output.strip())
