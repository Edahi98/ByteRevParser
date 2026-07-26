import gc
import os

from llama_cpp import Llama

from services.text_normalizer_service import TextNormalizerService

MODELS_AI_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models_ai")
GGUF_PATH = os.path.join(MODELS_AI_DIR, "qwen2.5-0.5b-instruct-q8_0.gguf")

_strip_accents = TextNormalizerService.strip_accents

SYSTEM_PROMPT = _strip_accents(
    "Redactas en prosa fluida y natural el contenido de una tabla en Markdown, usando "
    "exactamente los valores de cada fila (texto, número, fecha o cualquier otro tipo de dato), "
    "sin inventar ni omitir ningún valor, columna ni dato adicional. Una fila puede tener "
    "cualquier cantidad de columnas. "
    "Escribe una oración conectada y natural por fila, en su propia línea — no una lista "
    "mecánica de 'Columna 1 es X, Columna 2 es Y' ni fórmulas repetitivas como 'corresponde a'. "
    "Las columnas vienen etiquetadas genéricamente (Columna 1, Columna 2, Columna 3...). Si la "
    "primera fila de datos contiene palabras cortas que parecen ser el nombre real de cada "
    "columna, úsalas al redactar en vez de la etiqueta genérica, y no la describas como un dato "
    "más. Si ninguna fila parece encabezado, no menciones las etiquetas genéricas de columna en "
    "absoluto. "
    "No inventes ningún dato, descripción, opinión, diálogo ni contexto que no esté literalmente "
    "en la tabla (nada de personajes, apariencia física, emociones ni historias de ficción). Solo "
    "redacta con fluidez los datos reales tal cual aparecen. "
    "Si el texto recibido no es una tabla sino un párrafo normal, repítelo tal cual, sin "
    "modificarlo ni resumirlo."
)

EXAMPLE_TABLE_WITH_HEADER = (
    "| Columna 1 | Columna 2 |\n| --- | --- |\n| PRODUCTO | PRECIO |\n| Manzana | 10 |\n| Pan | 5 |"
)
EXAMPLE_PROSE_WITH_HEADER = "Manzana tiene un precio de 10.\nPan tiene un precio de 5."

EXAMPLE_TABLE_NO_HEADER = _strip_accents(
    "| Columna 1 | Columna 2 |\n| --- | --- |\n| ALMA CHONTAL | F |\n| RICARDO AVILA | M |"
)
EXAMPLE_PROSE_NO_HEADER = _strip_accents(
    "ALMA CHONTAL tiene asociado el valor F.\nRICARDO AVILA tiene asociado el valor M."
)

EXAMPLE_TABLE_NO_HEADER_MULTI = _strip_accents(
    "| Columna 1 | Columna 2 | Columna 3 |\n| --- | --- | --- |\n"
    "| 2024-01-05 | Compra | 1500 |\n| 2024-02-10 | Venta | 800 |"
)
EXAMPLE_PROSE_NO_HEADER_MULTI = _strip_accents(
    "El 2024-01-05 se registró Compra con un valor de 1500.\nEl 2024-02-10 se registró Venta con un valor de 800."
)

EXAMPLE_PARAGRAPH = _strip_accents(
    "Este documento fue generado el 12 de marzo de 2024 por el departamento de finanzas."
)
EXAMPLE_PARAGRAPH_PROSE = _strip_accents(
    "Este documento fue generado el 12 de marzo de 2024 por el departamento de finanzas."
)


class RedactorService:
    """Redacta texto narrativo a partir de contenido en Markdown (tablas), para que un
    modelo extractivo (NuExtract) tenga menos ambigüedad al alinear columna y valor.

    Singleton de una sola instancia por proceso, pero el modelo
    (qwen2.5-0.5b-instruct-q5_0.gguf) ya no se mantiene cargado entre llamadas:
    `redact()` lo carga bajo demanda vía llama.cpp (`llama_cpp.Llama`) y lo libera
    de memoria justo después de usarlo.

    El vocabulario de este .gguf corrompe tildes y la `ñ` al tokenizar (se
    reproduce igual con `transformers` y con llama.cpp nativo, así que es un
    problema del propio archivo, no del loader). Mientras se use este .gguf,
    `TextNormalizerService.strip_accents` limpia la entrada y la salida del
    modelo para evitar esa corrupción, a costa de perder el diacrítico original.
    """

    _instance: "RedactorService | None" = None

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

    def redact(self, markdown: str) -> str:
        self._load()
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": EXAMPLE_TABLE_WITH_HEADER},
                {"role": "assistant", "content": EXAMPLE_PROSE_WITH_HEADER},
                {"role": "user", "content": EXAMPLE_TABLE_NO_HEADER},
                {"role": "assistant", "content": EXAMPLE_PROSE_NO_HEADER},
                {"role": "user", "content": EXAMPLE_TABLE_NO_HEADER_MULTI},
                {"role": "assistant", "content": EXAMPLE_PROSE_NO_HEADER_MULTI},
                {"role": "user", "content": EXAMPLE_PARAGRAPH},
                {"role": "assistant", "content": EXAMPLE_PARAGRAPH_PROSE},
                {"role": "user", "content": TextNormalizerService.strip_accents(markdown)},
            ]
            response = self.llm.create_chat_completion(messages=messages, max_tokens=1024, temperature=0)
            output = response["choices"][0]["message"]["content"]
        finally:
            self._unload()

        return TextNormalizerService.strip_accents(output.strip())
