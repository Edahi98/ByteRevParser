from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer

from models.text_classifier_config import TextClassifierConfig
from services.text_classifier.word2vec_vectorizer import Word2VecVectorizer


class NoveltyPipelineFactory:
    """Construye el pipeline (Word2Vec + IsolationForest) que detecta frases fuera de dominio.

    A diferencia del pipeline clasificador, aquí NO se usa TF-IDF: con
    tan pocos ejemplos de entrenamiento, un espacio disperso de miles de
    dimensiones (TF-IDF) hace que IsolationForest no logre distinguir
    nada (todo queda marcado como normal). El espacio denso de Word2Vec
    sí funciona para esto. Se entrena sin las etiquetas del clasificador
    y marca como anómala (-1) cualquier frase que no se parezca a
    ninguna de las vistas en entrenamiento, para limpiarla antes de que
    llegue al clasificador.
    """

    @staticmethod
    def create(config: TextClassifierConfig) -> Pipeline:
        return Pipeline([
            (
                "vectorizer",
                Word2VecVectorizer(
                    vector_size=config.word2vec.vector_size,
                    window=config.word2vec.window,
                    min_count=config.word2vec.min_count,
                    sg=config.word2vec.sg,
                    seed=config.random_seed,
                ),
            ),
            ("normalize", Normalizer()),
            ("detector", IsolationForest(random_state=config.random_seed)),
        ])
