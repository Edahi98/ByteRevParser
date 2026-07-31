from typing import Callable

import numpy as np
import torch
from sklearn.base import BaseEstimator, TransformerMixin
from torch import optim

from services.detector_cambios_service.contrastive_loss_module import ContrastiveLossModule
from services.detector_cambios_service.deep_siamese_encoder_module import DeepSiameseEncoderModule
from services.detector_cambios_service.phrase_pair_sampler import PhrasePairSampler

INFERENCE_CHUNK_SIZE = 512


class DetectorCambiosEncoder(BaseEstimator, TransformerMixin):
    """Transformer de scikit-learn que entrena y usa un encoder profundo (Transformer de caracteres) para detectar frases de control de cambios equivalentes.

    `fit(X, y)` recibe secuencias de índices de caracteres ya tokenizadas
    por `CharTokenizer` (no una matriz TF-IDF: la representación de cada
    frase la aprende `DeepSiameseEncoderModule` de punta a punta) y, en
    `y`, el `origin_id` de cada fila — el vínculo con la frase original
    de la que salió, no una clase a predecir. Aprovecha el mecanismo
    estándar `Pipeline.fit(X, y)` de scikit-learn para propagar esa
    información hasta aquí. Por dentro entrena por mini-lotes sobre
    pares (frase, frase) armados por `PhrasePairSampler`, minimizando
    una pérdida contrastiva: pares del mismo origen quedan cerca en el
    embedding, pares de origen distinto quedan lejos. Al terminar,
    guarda `similarity_threshold_` (punto medio entre la distancia
    promedio de pares positivos y negativos) para que el caller pueda
    decidir "mismo cambio o no" comparando contra ese umbral.
    """

    def __init__(
        self,
        embed_dim: int = 64,
        num_layers: int = 3,
        num_heads: int = 4,
        ff_dim: int = 128,
        embedding_dim: int = 100,
        max_length: int = 160,
        dropout: float = 0.1,
        margin: float = 1.0,
        epochs: int = 20,
        batch_size: int = 64,
        learning_rate: float = 0.001,
        pairs_per_anchor: int = 2,
        seed: int = 42,
        progress_callback: Callable[[int, int], None] | None = None,
    ):
        self.embed_dim = embed_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.embedding_dim = embedding_dim
        self.max_length = max_length
        self.dropout = dropout
        self.margin = margin
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.pairs_per_anchor = pairs_per_anchor
        self.seed = seed
        self.progress_callback = progress_callback

    def fit(self, X, y=None):
        if y is None:
            raise ValueError("DetectorCambiosEncoder.fit necesita 'y' con el origin_id de cada fila.")

        origin_ids = np.asarray(y)
        rng = np.random.default_rng(self.seed)
        torch.manual_seed(self.seed)

        vocab_size = int(X.max()) + 1
        self.device_ = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_ = DeepSiameseEncoderModule(
            vocab_size=vocab_size,
            embed_dim=self.embed_dim,
            num_layers=self.num_layers,
            num_heads=self.num_heads,
            ff_dim=self.ff_dim,
            embedding_dim=self.embedding_dim,
            max_length=self.max_length,
            dropout=self.dropout,
        ).to(self.device_)

        optimizador = optim.Adam(self.model_.parameters(), lr=self.learning_rate)
        funcion_perdida = ContrastiveLossModule(margin=self.margin)
        sampler = PhrasePairSampler()

        self.model_.train()
        for epoca in range(self.epochs):
            anclas, pares, etiquetas = sampler.build_pairs(origin_ids, self.pairs_per_anchor, rng)
            orden = rng.permutation(len(anclas))

            for inicio in range(0, len(orden), self.batch_size):
                lote_orden = orden[inicio : inicio + self.batch_size]
                lote_a = self._a_tensor(X[anclas[lote_orden]])
                lote_b = self._a_tensor(X[pares[lote_orden]])
                lote_y = torch.as_tensor(etiquetas[lote_orden], device=self.device_)

                optimizador.zero_grad()
                embedding_a = self.model_(lote_a)
                embedding_b = self.model_(lote_b)
                perdida = funcion_perdida(embedding_a, embedding_b, lote_y)
                perdida.backward()
                optimizador.step()

            if self.progress_callback is not None:
                self.progress_callback(epoca + 1, self.epochs)

        self._calibrar_umbral(X, origin_ids, rng)
        return self

    def transform(self, X) -> np.ndarray:
        self.model_.eval()
        embeddings = []
        with torch.no_grad():
            for lote in self._a_lotes(X):
                embeddings.append(self.model_(self._a_tensor(lote)).cpu().numpy())
        return np.vstack(embeddings)

    def nearest_reference(self, embeddings: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Para cada embedding, devuelve (distancia, índice) al vecino más cercano en `reference_embeddings_`.

        Compara por lotes contra el banco de referencia completo en vez
        de construir una sola matriz `n_nuevas x n_referencia` de una
        vez, para no disparar el uso de memoria cuando ambos lados son
        grandes (p. ej. un CSV de 10,000 frases nuevas contra un banco de
        10,000 frases de referencia serían 100 millones de floats).
        """
        distancias_minimas = []
        indices_mas_cercanos = []
        for inicio in range(0, len(embeddings), INFERENCE_CHUNK_SIZE):
            lote = embeddings[inicio : inicio + INFERENCE_CHUNK_SIZE]
            distancias_lote = np.linalg.norm(lote[:, None, :] - self.reference_embeddings_[None, :, :], axis=2)
            indices_lote = np.argmin(distancias_lote, axis=1)
            distancias_minimas.append(distancias_lote[np.arange(len(lote)), indices_lote])
            indices_mas_cercanos.append(indices_lote)

        return np.concatenate(distancias_minimas), np.concatenate(indices_mas_cercanos)

    def _calibrar_umbral(self, X, origin_ids: np.ndarray, rng: np.random.Generator) -> None:
        sampler = PhrasePairSampler()
        anclas, pares, etiquetas = sampler.build_pairs(origin_ids, self.pairs_per_anchor, rng)

        embeddings = self.transform(X)
        distancias = np.linalg.norm(embeddings[anclas] - embeddings[pares], axis=1)

        distancias_positivas = distancias[etiquetas == 1]
        distancias_negativas = distancias[etiquetas == 0]

        self.mean_distance_positive_ = float(distancias_positivas.mean())
        self.mean_distance_negative_ = float(distancias_negativas.mean())
        self.similarity_threshold_ = (self.mean_distance_positive_ + self.mean_distance_negative_) / 2

        aciertos_positivos = (distancias_positivas <= self.similarity_threshold_).mean()
        aciertos_negativos = (distancias_negativas > self.similarity_threshold_).mean()
        self.pair_accuracy_ = float((aciertos_positivos + aciertos_negativos) / 2)

    def _a_lotes(self, X):
        n_muestras = X.shape[0]
        for inicio in range(0, n_muestras, INFERENCE_CHUNK_SIZE):
            yield X[inicio : inicio + INFERENCE_CHUNK_SIZE]

    def _a_tensor(self, lote) -> torch.Tensor:
        return torch.as_tensor(np.asarray(lote, dtype=np.int64), device=self.device_)
