import polars as pl

REQUIRED_COLUMN = "frase"


class DetectorCambiosBatchService:
    """Compara en lote frases nuevas leídas desde un CSV con polars contra el banco de frases de control de cambios aprendidas.

    Usa un pipeline de detección ya entrenado, igual que
    `DetectorCambiosService` pero de forma vectorizada: calcula todos
    los embeddings de una vez y busca el vecino más cercano de cada uno
    por lotes (`DetectorCambiosEncoder.nearest_reference`).
    """

    def compare_from_csv(self, csv_path: str, pipeline) -> list[dict]:
        df_nuevas = pl.read_csv(csv_path)

        if REQUIRED_COLUMN not in df_nuevas.columns:
            raise ValueError(f"El CSV de frases nuevas debe tener una columna '{REQUIRED_COLUMN}'.")

        frases_nuevas = df_nuevas.get_column(REQUIRED_COLUMN).to_list()

        encoder = pipeline.named_steps["encoder"]
        embeddings = pipeline.transform(frases_nuevas)
        distancias, indices_mas_cercanos = encoder.nearest_reference(embeddings)

        resultados = []
        for frase, distancia, indice_mas_cercano in zip(frases_nuevas, distancias, indices_mas_cercanos):
            resultados.append(
                {
                    "frase": frase,
                    "es_conocida": bool(distancia <= encoder.similarity_threshold_),
                    "distancia": float(distancia),
                    "frase_mas_parecida": str(encoder.reference_phrases_[indice_mas_cercano]),
                }
            )

        return resultados
