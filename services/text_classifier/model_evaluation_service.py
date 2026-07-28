import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score

NUM_FOLDS = 5
RANDOM_SEED = 42


class ModelEvaluationService:
    """Evalúa un modelo con validación cruzada estratificada y un classification report."""

    def evaluate(self, model, X: np.ndarray, y: np.ndarray) -> dict:
        cv = StratifiedKFold(n_splits=NUM_FOLDS, shuffle=True, random_state=RANDOM_SEED)
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
