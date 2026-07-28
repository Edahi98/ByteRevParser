from services.text_classifier.feature_service import FeatureService
from services.text_classifier.spanish_stopwords_service import SpanishStopwordsService
from services.text_classifier.tokenizer_service import TokenizerService
from services.text_classifier.word2vec_service import Word2VecService


class TextClassificationService:
    """Clasifica frases usando artefactos (modelo, TF-IDF, Word2Vec) cargados en memoria.

    Singleton de una sola instancia por proceso. No lee ni escribe nada en
    disco: `load_artifacts()` recibe los objetos ya deserializados (por
    ejemplo, a partir de un ZIP exportado por `/train_text_classifier` y
    subido de vuelta por el cliente) y los deja listos para `classify()`.
    """

    _instance: "TextClassificationService | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.tokenizer_service = TokenizerService()
        self.word2vec_service = Word2VecService(self.tokenizer_service)
        self.feature_service = FeatureService(self.word2vec_service, SpanishStopwordsService())
        self.model = None
        self._initialized = True

    def load_artifacts(self, model, tfidf, word2vec_model) -> None:
        self.model = model
        self.feature_service.use_fitted_tfidf(tfidf)
        self.word2vec_service.use_trained_model(word2vec_model)

    def classify(self, phrase: str) -> str:
        X = self.feature_service.build([phrase])
        return str(self.model.predict(X)[0])
