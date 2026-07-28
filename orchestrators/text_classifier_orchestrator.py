import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

from services.text_classifier.dataset_service import DatasetService
from services.text_classifier.feature_service import FeatureService
from services.text_classifier.model_evaluation_service import ModelEvaluationService
from services.text_classifier.spanish_stopwords_service import SpanishStopwordsService
from services.text_classifier.tokenizer_service import TokenizerService
from services.text_classifier.word2vec_service import Word2VecService

RANDOM_SEED = 42


class TextClassifierOrchestrator:
    """Orquesta el entrenamiento completo: dataset -> features -> modelos -> artefactos entrenados.

    No persiste nada en disco: devuelve el modelo, el TF-IDF y el Word2Vec
    ya entrenados junto con el reporte de evaluación, para que el caller
    decida cómo exportarlos (p. ej. empaquetados en un ZIP descargable).
    """

    def __init__(self):
        self.dataset_service = DatasetService()
        self.tokenizer_service = TokenizerService()
        self.word2vec_service = Word2VecService(self.tokenizer_service)
        self.feature_service = FeatureService(self.word2vec_service, SpanishStopwordsService())
        self.evaluation_service = ModelEvaluationService()

    def run(self, csv_path: str) -> dict:
        df_etiquetado = self.dataset_service.load_labeled(csv_path)
        frases_etiquetadas = df_etiquetado.get_column("frase").to_list()
        etiquetas = np.array(df_etiquetado.get_column("etiqueta").to_list())
        distribucion_clases = self.dataset_service.class_distribution(df_etiquetado)

        self.word2vec_service.train(frases_etiquetadas)
        self.feature_service.fit(frases_etiquetadas)

        X = self.feature_service.build(frases_etiquetadas)

        modelo_rf = RandomForestClassifier(random_state=RANDOM_SEED)
        modelo_gb = GradientBoostingClassifier(random_state=RANDOM_SEED)

        resultados_rf = self.evaluation_service.evaluate(modelo_rf, X, etiquetas)
        resultados_gb = self.evaluation_service.evaluate(modelo_gb, X, etiquetas)

        modelo_final = modelo_rf

        report = {
            "clases": distribucion_clases,
            "resultados_cv": {
                "RandomForestClassifier": resultados_rf,
                "GradientBoostingClassifier": resultados_gb,
            },
        }

        return {
            "model": modelo_final,
            "tfidf": self.feature_service.tfidf,
            "word2vec_model": self.word2vec_service.model,
            "report": report,
        }
