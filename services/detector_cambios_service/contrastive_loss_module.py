import torch
from torch import nn


class ContrastiveLossModule(nn.Module):
    """Pérdida contrastiva clásica (Hadsell et al.) sobre pares de embeddings.

    Para un par con etiqueta 1 (mismo origen) minimiza la distancia entre
    ambos embeddings; para un par con etiqueta 0 (origen distinto) la
    empuja a ser al menos `margin`, sin penalizar más allá de ese margen.
    """

    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin

    def forward(self, embedding_a: torch.Tensor, embedding_b: torch.Tensor, label: torch.Tensor) -> torch.Tensor:
        distancia = torch.norm(embedding_a - embedding_b, p=2, dim=1)
        perdida_positiva = label * distancia.pow(2)
        perdida_negativa = (1 - label) * torch.clamp(self.margin - distancia, min=0.0).pow(2)
        return (perdida_positiva + perdida_negativa).mean()
