from torch import nn


class TextAutoencoderModule(nn.Module):
    """Red neuronal encoder-decoder: aprende una reducción de dimensionalidad no lineal del TF-IDF.

    El encoder comprime el vector TF-IDF de cada frase a un espacio denso
    de `bottleneck_dim`; el decoder intenta reconstruir el vector
    original desde ese espacio. Qué tan bien logra reconstruirlo es, en
    sí mismo, una señal de qué tan "típica" es esa frase para lo que el
    modelo aprendió a reconocer.
    """

    def __init__(self, input_dim: int, hidden_dim: int, bottleneck_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, bottleneck_dim),
        )
        self.decoder = nn.Sequential(
            nn.Linear(bottleneck_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
        )

    def forward(self, x):
        embedding = self.encoder(x)
        reconstruccion = self.decoder(embedding)
        return embedding, reconstruccion
