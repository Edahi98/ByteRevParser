import glob
import os

import polars as pl

DEFAULT_HARD_NEGATIVES_DIR = os.path.join("data", "generador_nlp", "datasets", "negativos")


class HardNegativeService:
    """Carga frases genuinamente ajenas al dominio de entrenamiento, para usarlas como negativos explícitos.

    Sin esto, el modelo solo ve negativos que vienen del mismo corpus
    (frases de otro `origin_id` pero del mismo dominio de control de
    cambios) y nunca aprende una frontera real contra contenido de otro
    tema por completo — una frase ajena podía colarse como "conocida"
    con tal de compartir algunas palabras/fragmentos de caracteres con
    el corpus. Cada archivo CSV dentro de
    `data/generador_nlp/datasets/negativos/` aporta frases de una fuente
    distinta (p. ej. reseñas de productos,
    instructivos paso a paso) — todos con columna `frase` únicamente,
    sin `origin_id` propio: cada fila recibe uno nuevo, disjunto de los
    reales y sin compañeros, para que `PhrasePairSampler` nunca la use
    como positivo, solo como negativo explícito durante el entrenamiento
    contrastivo. Si la carpeta está vacía (o no existe), se omite
    silenciosamente (el entrenamiento sigue funcionando sin negativos
    externos).
    """

    def load(self, existing_origin_ids: list[int], directory: str = DEFAULT_HARD_NEGATIVES_DIR) -> tuple[list[str], list[int]]:
        frases: list[str] = []
        for csv_path in sorted(glob.glob(os.path.join(directory, "*.csv"))):
            df = pl.read_csv(csv_path)
            frases.extend(df.get_column("frase").to_list())

        if not frases:
            return [], []

        siguiente_id = max(existing_origin_ids) + 1 if existing_origin_ids else 0
        origin_ids = list(range(siguiente_id, siguiente_id + len(frases)))

        return frases, origin_ids
