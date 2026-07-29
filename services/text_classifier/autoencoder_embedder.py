import numpy as np
import torch
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin
from torch import nn, optim

from services.text_classifier.text_autoencoder_module import TextAutoencoderModule

INFERENCE_CHUNK_SIZE = 512


class AutoencoderEmbedder(BaseEstimator, TransformerMixin):
    """Transformer de scikit-learn que entrena y usa un autoencoder de PyTorch para reducir dimensionalidad.

    Reemplaza a `TruncatedSVD` con una reducción no lineal aprendida por
    backpropagation, encajando en el mismo lugar de un `Pipeline` (mismo
    contrato `fit`/`transform`/`inverse_transform`). Entrena por
    mini-lotes, densificando solo un lote a la vez desde la matriz TF-IDF
    dispersa, para no materializar la matriz completa en memoria (con
    vocabularios grandes eso puede pesar gigabytes). Además de la
    reducción, guarda el error de reconstrucción del propio dataset de
    entrenamiento y un umbral basado en `contamination`, para que el
    caller pueda usar `reconstruction_error()` como una segunda señal de
    ruido, complementaria a `IsolationForest`.
    """

    def __init__(
        self,
        hidden_dim: int = 256,
        bottleneck_dim: int = 100,
        epochs: int = 15,
        batch_size: int = 64,
        learning_rate: float = 0.001,
        contamination: float | str = 0.05,
        seed: int = 42,
    ):
        self.hidden_dim = hidden_dim
        self.bottleneck_dim = bottleneck_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.contamination = contamination
        self.seed = seed

    def fit(self, X, y=None):
        torch.manual_seed(self.seed)
        self.device_ = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_ = TextAutoencoderModule(X.shape[1], self.hidden_dim, self.bottleneck_dim).to(self.device_)

        optimizador = optim.Adam(self.model_.parameters(), lr=self.learning_rate)
        funcion_perdida = nn.MSELoss()
        n_muestras = X.shape[0]

        self.model_.train()
        for _ in range(self.epochs):
            indices = np.random.permutation(n_muestras)
            for inicio in range(0, n_muestras, self.batch_size):
                lote_indices = indices[inicio : inicio + self.batch_size]
                lote = self._a_tensor(X[lote_indices])

                optimizador.zero_grad()
                _, reconstruccion = self.model_(lote)
                perdida = funcion_perdida(reconstruccion, lote)
                perdida.backward()
                optimizador.step()

        self.reconstruction_errors_ = self.reconstruction_error(X)
        contaminacion = self.contamination if isinstance(self.contamination, (int, float)) else 0.05
        self.error_umbral_ = float(np.percentile(self.reconstruction_errors_, 100 * (1 - contaminacion)))

        return self

    def transform(self, X) -> np.ndarray:
        self.model_.eval()
        embeddings = []
        with torch.no_grad():
            for lote in self._a_lotes(X):
                embedding, _ = self.model_(self._a_tensor(lote))
                embeddings.append(embedding.cpu().numpy())
        return np.vstack(embeddings)

    def inverse_transform(self, embeddings: np.ndarray) -> np.ndarray:
        self.model_.eval()
        with torch.no_grad():
            tensor = torch.as_tensor(np.asarray(embeddings, dtype=np.float32), device=self.device_)
            reconstruccion = self.model_.decoder(tensor)
        return reconstruccion.cpu().numpy()

    def reconstruction_error(self, X) -> np.ndarray:
        self.model_.eval()
        errores = []
        with torch.no_grad():
            for lote in self._a_lotes(X):
                tensor = self._a_tensor(lote)
                _, reconstruccion = self.model_(tensor)
                error_por_fila = torch.mean((reconstruccion - tensor) ** 2, dim=1)
                errores.append(error_por_fila.cpu().numpy())
        return np.concatenate(errores)

    def _a_lotes(self, X):
        n_muestras = X.shape[0]
        for inicio in range(0, n_muestras, INFERENCE_CHUNK_SIZE):
            yield X[inicio : inicio + INFERENCE_CHUNK_SIZE]

    def _a_tensor(self, lote) -> torch.Tensor:
        denso = lote.toarray() if sparse.issparse(lote) else lote
        denso = np.asarray(denso, dtype=np.float32)
        return torch.from_numpy(denso).to(self.device_)
