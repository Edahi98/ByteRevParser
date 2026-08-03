class ValidDataFilterService:
    """Deja en `valid_data` solo los valores que el detector de control de cambios aprueba.

    Recibe la estructura tal cual sale de `TsubasaService.execute` (la misma
    que consume `XmlService.prune_xml`, de ahí el tipo `dict | list`), evalúa
    cada valor hoja con el encoder y descarta los que no llegan al umbral. La
    forma se conserva: solo desaparecen las entradas rechazadas y los
    contenedores que se quedan sin contenido.

    `restrict` compara por igualdad literal a propósito: los conjuntos que
    recibe ya vienen expresados con los valores tal cual salen del pipeline
    (`ChangeScopeService` se encarga de reconciliarlos con el texto del XML
    usando el criterio de `XmlService`), así que aquí no hace falta —ni debe
    haber— ninguna normalización propia.
    """

    _DISCARD = object()

    def filter(self, valid_data: dict | list, encoder) -> dict | list:
        texts = self.collect_texts(valid_data)
        if not texts:
            return valid_data

        # Una sola llamada a `predict`: el encoder recarga jina-embeddings-v3
        # (~1.6GB) en cada invocación, así que todo el lote se evalúa junto en
        # vez de valor por valor.
        es_cambio, _ = encoder.predict(texts)
        approved = {text for text, is_cambio in zip(texts, es_cambio) if is_cambio}

        return self.restrict(valid_data, approved)

    def restrict(self, valid_data: dict | list, allowed: set[str]) -> dict | list:
        """Poda `valid_data` dejando solo los valores presentes en `allowed`."""
        pruned = self._prune(valid_data, allowed)
        if pruned is self._DISCARD:
            return {} if isinstance(valid_data, dict) else []

        return pruned

    def collect_texts(self, valid_data: dict | list) -> list[str]:
        collected: list[str] = []
        self._collect_into(valid_data, collected)

        # `dict.fromkeys` deduplica conservando el orden: un texto repetido no
        # se manda dos veces al modelo.
        return list(dict.fromkeys(collected))

    def _collect_into(self, node, collected: list[str]) -> None:
        if isinstance(node, dict):
            for value in node.values():
                self._collect_into(value, collected)
        elif isinstance(node, list):
            for value in node:
                self._collect_into(value, collected)
        elif node is not None:
            collected.append(str(node))

    def _prune(self, node, approved: set[str]):
        if isinstance(node, dict):
            pruned_dict = {}
            for key, value in node.items():
                child = self._prune(value, approved)
                if child is not self._DISCARD:
                    pruned_dict[key] = child
            return pruned_dict or self._DISCARD

        if isinstance(node, list):
            pruned_list = [
                child for child in (self._prune(value, approved) for value in node) if child is not self._DISCARD
            ]
            return pruned_list or self._DISCARD

        if node is None:
            return self._DISCARD

        return node if str(node) in approved else self._DISCARD
