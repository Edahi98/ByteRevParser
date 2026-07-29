from sklearn.ensemble import IsolationForest

from models.text_classifier_config import TextClassifierConfig


class IsolationForestFactory:
    """Construye el detector de frases anómalas/rotas usado como filtro de ruido.

    Un `staticmethod` en vez de una función suelta, siguiendo el mismo
    patrón de fábrica que `BinaryAdapterFactory`. Se entrena sobre el
    mismo espacio denso de features (TF-IDF char_wb + SVD) que usa el
    agrupador, ya que ese espacio reducido no sufre la maldición de la
    dimensionalidad que sí afectaba a un TF-IDF disperso sin reducir.
    """

    @staticmethod
    def create(config: TextClassifierConfig) -> IsolationForest:
        return IsolationForest(contamination=config.novelty.contamination, random_state=config.random_seed)
