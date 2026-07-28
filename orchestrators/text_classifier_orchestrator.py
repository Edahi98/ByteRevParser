import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from services.text_classifier.config_loader_service import ConfigLoaderService
from services.text_classifier.dataset_service import DatasetService
from services.text_classifier.feature_pipeline_factory import FeaturePipelineFactory
from services.text_classifier.model_calibration_service import ModelCalibrationService
from services.text_classifier.model_evaluation_service import ModelEvaluationService
from services.text_classifier.novelty_pipeline_factory import NoveltyPipelineFactory


class TextClassifierOrchestrator:
    """Orquesta el entrenamiento completo: dataset -> pipelines candidatos -> mejor modelo.

    Cada candidato es un Pipeline de scikit-learn completo (features +
    clasificador calibrado), evaluado por separado con validación cruzada
    para evitar fuga de datos entre folds. No persiste nada en disco:
    devuelve el pipeline ganador junto con el reporte de evaluación, para
    que el caller decida cómo exportarlo (p. ej. un ZIP descargable).
    Todos los hiperparámetros vienen de `config/text_classifier_config.json`
    (vía `ConfigLoaderService`), no están fijos en el código, para que el
    mismo clasificador sirva para otros datasets sin tocar Python.
    """

    def __init__(self):
        self.dataset_service = DatasetService()
        self.evaluation_service = ModelEvaluationService()
        self.calibration_service = ModelCalibrationService()
        self.config = ConfigLoaderService().load()

    def run(self, csv_path: str) -> dict:
        df_etiquetado = self.dataset_service.load_labeled(csv_path)
        frases_etiquetadas = df_etiquetado.get_column("frase").to_list()
        etiquetas = np.array(df_etiquetado.get_column("etiqueta").to_list())
        distribucion_clases = self.dataset_service.class_distribution(df_etiquetado)

        candidatos = self._build_candidate_pipelines()

        resultados_cv = {}
        for nombre, pipeline in candidatos.items():
            resultados_cv[nombre] = self.evaluation_service.evaluate(
                pipeline, frases_etiquetadas, etiquetas, self.config
            )

        nombre_ganador = max(resultados_cv, key=lambda nombre: resultados_cv[nombre]["f1_macro_promedio"])
        pipeline_final = candidatos[nombre_ganador]

        pipeline_novedad = NoveltyPipelineFactory.create(self.config)
        pipeline_novedad.fit(frases_etiquetadas)

        report = {
            "clases": distribucion_clases,
            "modelo_exportado": nombre_ganador,
            "resultados_cv": resultados_cv,
        }

        return {"model": pipeline_final, "novelty_model": pipeline_novedad, "report": report}

    def _build_candidate_pipelines(self) -> dict[str, Pipeline]:
        class_weight = self.config.classifiers.class_weight
        random_seed = self.config.random_seed

        modelo_rf = self.calibration_service.calibrate(
            RandomForestClassifier(random_state=random_seed, class_weight=class_weight), self.config
        )
        # GradientBoostingClassifier no acepta class_weight en scikit-learn.
        modelo_gb = self.calibration_service.calibrate(
            GradientBoostingClassifier(random_state=random_seed), self.config
        )
        modelo_svm = self.calibration_service.calibrate(
            LinearSVC(random_state=random_seed, class_weight=class_weight), self.config
        )

        return {
            "RandomForestClassifier": Pipeline([
                ("features", FeaturePipelineFactory.create(self.config)),
                ("classifier", modelo_rf),
            ]),
            "GradientBoostingClassifier": Pipeline([
                ("features", FeaturePipelineFactory.create(self.config)),
                ("classifier", modelo_gb),
            ]),
            "LinearSVC": Pipeline([
                ("features", FeaturePipelineFactory.create(self.config)),
                ("classifier", modelo_svm),
            ]),
        }
