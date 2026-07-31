import math

import torch
from torch import nn


class PositionalEncodingModule(nn.Module):
    """Codificación posicional seno/coseno estándar, para que el Transformer distinga el orden de los caracteres.

    La auto-atención por sí sola no sabe en qué posición está cada
    carácter de la secuencia — sin esto, "se cambia" y "cambia se"
    lucirían idénticos para el encoder.
    """

    def __init__(self, embed_dim: int, max_length: int):
        super().__init__()
        posicion = torch.arange(max_length).unsqueeze(1)
        divisor = torch.exp(torch.arange(0, embed_dim, 2) * (-math.log(10000.0) / embed_dim))
        codificacion = torch.zeros(max_length, embed_dim)
        codificacion[:, 0::2] = torch.sin(posicion * divisor)
        codificacion[:, 1::2] = torch.cos(posicion * divisor)
        self.register_buffer("codificacion", codificacion)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.codificacion[: x.size(1)]
