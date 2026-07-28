from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedKFold

from models.text_classifier_config import TextClassifierConfig


class ModelCalibrationService:
    """Envuelve un modelo sin entrenar en un CalibratedClassifierCV para calibrar sus probabilidades.

    El método y el número de folds vienen de `TextClassifierConfig`.
    Por defecto se usa sigmoid (Platt scaling) en vez de isotonic porque
    es más estable con pocos ejemplos por clase, y menos folds que la
    evaluación general para no exigir más muestras por clase de las que
    el dataset del caller pueda tener.
    """

    def calibrate(self, model, config: TextClassifierConfig) -> CalibratedClassifierCV:
        cv = StratifiedKFold(n_splits=config.calibration.folds, shuffle=True, random_state=config.random_seed)
        return CalibratedClassifierCV(estimator=model, method=config.calibration.method, cv=cv)
