import torch
import torch.nn.functional as F
from torch import nn

from services.detector_cambios_service.positional_encoding_module import PositionalEncodingModule


class DeepSiameseEncoderModule(nn.Module):
    """Encoder profundo entrenado desde cero: embeddings de caracteres + Transformer de varias capas + pooling.

    Reemplaza a TF-IDF seguido de una red de dos capas: aquí la
    representación de cada frase no es una bolsa fija de fragmentos de
    caracteres, la aprende una pila de capas de auto-atención sobre la
    secuencia completa, igual que arquitecturas modernas de NLP — pero
    entrenada por completo con las frases de este dataset, sin cargar
    ningún peso preentrenado. El promedio final ignora las posiciones de
    relleno (`padding_mask`) para que frases cortas no se diluyan contra
    el relleno usado para emparejar longitudes dentro de un lote.
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 64,
        num_layers: int = 3,
        num_heads: int = 4,
        ff_dim: int = 128,
        embedding_dim: int = 100,
        max_length: int = 160,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.positional_encoding = PositionalEncodingModule(embed_dim, max_length)
        capa_transformer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
        )
        # enable_nested_tensor=False: el "fast path" de tensores anidados de PyTorch
        # para máscaras de relleno es más lento en CPU en la práctica que el camino
        # normal, no más rápido — sin esto, 20 épocas sobre 11,000 frases tardaban
        # más de 2 horas.
        self.transformer = nn.TransformerEncoder(capa_transformer, num_layers=num_layers, enable_nested_tensor=False)
        self.proyeccion = nn.Linear(embed_dim, embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mascara_relleno = x == 0

        embebido = self.embedding(x)
        embebido = self.positional_encoding(embebido)
        codificado = self.transformer(embebido, src_key_padding_mask=mascara_relleno)

        mascara_valida = (~mascara_relleno).unsqueeze(-1).float()
        suma = (codificado * mascara_valida).sum(dim=1)
        conteo = mascara_valida.sum(dim=1).clamp(min=1)
        promedio = suma / conteo

        proyectado = self.proyeccion(promedio)
        return F.normalize(proyectado, p=2, dim=1)
