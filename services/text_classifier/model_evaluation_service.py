import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score

from models.text_classifier_config import TextClassifierConfig


class ModelEvaluationService:
    """Evalúa un pipeline (features + clasificador) con validación cruzada estratificada.

    X son las frases crudas: al recibir un Pipeline completo, cada fold de
    la validación cruzada reentrena también el TF-IDF y el Word2Vec solo
    con los datos de entrenamiento de ese fold, evitando fuga de datos
    hacia el fold de validación. El número de folds viene de
    `TextClassifierConfig`.
    """

    def evaluate(self, model, X: list[str], y: np.ndarray, config: TextClassifierConfig) -> dict:
        cv = StratifiedKFold(n_splits=config.evaluation.cv_folds, shuffle=True, random_state=config.random_seed)
        puntajes = cross_val_score(model, X, y, cv=cv, scoring="f1_macro")

        model.fit(X, y)
        predicciones = model.predict(X)
        reporte = classification_report(y, predicciones, output_dict=True)

        return {
            "f1_macro_por_fold": [float(puntaje) for puntaje in puntajes],
            "f1_macro_promedio": float(puntajes.mean()),
            "f1_macro_desviacion": float(puntajes.std()),
            "classification_report": reporte,
        }
