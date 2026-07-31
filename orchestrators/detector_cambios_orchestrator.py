from typing import Callable

import numpy as np

from models.detector_cambios_config import DetectorCambiosConfig
from services.detector_cambios_service.config_loader_service import ConfigLoaderService
from services.detector_cambios_service.dataset_service import DatasetService
from services.detector_cambios_service.feature_pipeline_factory import FeaturePipelineFactory
from services.detector_cambios_service.hard_negative_service import HardNegativeService
from services.detector_cambios_service.phrase_pair_sampler import PhrasePairSampler


class DetectorCambiosOrchestrator:
    """Orquesta el entrenamiento completo del detector de control de cambios: dataset -> features -> red siamesa -> banco de referencia.

    No necesita etiquetas de clase: usa el `origin_id` de cada frase (qué
    frase original generó esa variante ruidosa) para armar pares
    "hablan de lo mismo" / "hablan de cosas distintas" y entrenar la red
    contrastiva. Además de los negativos que salen del propio corpus
    (frases de otro `origin_id` pero del mismo dominio), suma frases
    genuinamente ajenas al dominio (`HardNegativeService`) como
    negativos explícitos — sin esto, el modelo nunca ve durante el
    entrenamiento un ejemplo de "esto no tiene nada que ver", y puede
    aceptar frases de otro tema con tal de compartir algo de vocabulario
    con el corpus. Esas frases ajenas se usan solo para moldear la
    frontera de decisión: se excluyen del banco de referencia final, así
    que nunca aparecen como "frase más parecida" en una comparación real.
    Al terminar, fija el banco de referencia (embeddings + frases reales
    de entrenamiento) directamente en el encoder ya ajustado, para que
    `DetectorCambiosService`/`DetectorCambiosBatchService` puedan
    comparar frases nuevas contra él. No persiste nada en disco: devuelve
    el pipeline junto con el reporte, para que el caller decida cómo
    exportarlo (p. ej. un ZIP descargable).
    """

    def __init__(self):
        self.dataset_service = DatasetService()
        self.pair_sampler = PhrasePairSampler()
        self.hard_negative_service = HardNegativeService()
        self.config = ConfigLoaderService().load()

    def run(
        self,
        csv_path: str,
        config: DetectorCambiosConfig | None = None,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> dict:
        config = config or self.config

        df = self.dataset_service.load(csv_path)
        frases_reales = df.get_column("frase").to_list()
        origin_ids_reales = np.array(df.get_column("origin_id").to_list())
        n_reales = len(frases_reales)

        frases_ajenas, origin_ids_ajenas = self.hard_negative_service.load(origin_ids_reales.tolist())

        frases_todas = frases_reales + frases_ajenas
        origin_ids_todas = np.concatenate(
            [origin_ids_reales, np.array(origin_ids_ajenas, dtype=origin_ids_reales.dtype)]
        )

        features = FeaturePipelineFactory.create(config, progress_callback)
        embeddings_todas = features.fit_transform(frases_todas, origin_ids_todas)

        encoder = features.named_steps["encoder"]
        encoder.reference_embeddings_ = embeddings_todas[:n_reales]
        encoder.reference_phrases_ = np.array(frases_reales)

        report = self._build_report(
            encoder, embeddings_todas, origin_ids_todas, origin_ids_reales, n_reales, len(frases_ajenas), config
        )

        return {"model": features, "report": report}

    def _build_report(
        self,
        encoder,
        embeddings_todas: np.ndarray,
        origin_ids_todas: np.ndarray,
        origin_ids_reales: np.ndarray,
        n_reales: int,
        n_ajenas: int,
        config: DetectorCambiosConfig,
    ) -> dict:
        rng = np.random.default_rng(config.random_seed + 1)
        anclas, pares, etiquetas = self.pair_sampler.build_pairs(origin_ids_todas, config.siamese.pairs_per_anchor, rng)

        distancias = np.linalg.norm(embeddings_todas[anclas] - embeddings_todas[pares], axis=1)
        aciertos_positivos = (distancias[etiquetas == 1] <= encoder.similarity_threshold_).mean()
        aciertos_negativos = (distancias[etiquetas == 0] > encoder.similarity_threshold_).mean()

        return {
            "n_frases": n_reales,
            "n_frases_origen": int(len(np.unique(origin_ids_reales))),
            "n_negativos_ajenos": n_ajenas,
            "distancia_promedio_positivos": encoder.mean_distance_positive_,
            "distancia_promedio_negativos": encoder.mean_distance_negative_,
            "umbral_similitud": encoder.similarity_threshold_,
            "precision_separacion": float((aciertos_positivos + aciertos_negativos) / 2),
            "configuracion_usada": config.model_dump(),
        }
