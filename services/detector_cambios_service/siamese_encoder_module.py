import torch.nn.functional as F
from torch import nn


class SiameseEncoderModule(nn.Module):
    """Torre única de encoder aplicada dos veces con los mismos pesos a cada mitad de un par.

    Comprime el vector TF-IDF de cada frase a un espacio denso de
    `embedding_dim`, normalizado a norma unitaria (`F.normalize`) para que
    la distancia euclidiana entre dos embeddings sea equivalente a su
    similitud coseno. Es "siamesa" porque el mismo `forward` se llama una
    vez por cada frase del par durante el entrenamiento contrastivo, sin
    ninguna copia de pesos.
    """

    def __init__(self, input_dim: int, hidden_dim: int, embedding_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embedding_dim),
        )

    def forward(self, x):
        embedding = self.encoder(x)
        return F.normalize(embedding, p=2, dim=1)
