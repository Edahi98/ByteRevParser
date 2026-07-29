from models.text_classifier_config import TextClassifierConfig


class ConfigOverrideService:
    """Combina la configuración por defecto con overrides parciales enviados por el cliente.

    Los overrides pueden traer solo algunos campos (p. ej. nada más
    `tfidf.max_features`); el resto se conserva de la configuración base,
    para que el panel de ajustes del frontend no tenga que enviar siempre
    el JSON completo.
    """

    def apply(self, base: TextClassifierConfig, overrides: dict) -> TextClassifierConfig:
        combinado = self._deep_merge(base.model_dump(), overrides)
        return TextClassifierConfig(**combinado)

    def _deep_merge(self, base: dict, overrides: dict) -> dict:
        resultado = dict(base)
        for clave, valor in overrides.items():
            if isinstance(valor, dict) and isinstance(resultado.get(clave), dict):
                resultado[clave] = self._deep_merge(resultado[clave], valor)
            else:
                resultado[clave] = valor
        return resultado
