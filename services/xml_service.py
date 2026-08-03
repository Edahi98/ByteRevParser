import os
import uuid

from bs4 import BeautifulSoup


class XmlService:
    """Extrae y poda contenido de archivos XML"""

    BOILERPLATE_TAGS = ("Footers", "Headers")

    def _strip_boilerplate(self, soup: BeautifulSoup) -> None:
        for tag in soup.find_all(self.BOILERPLATE_TAGS):
            tag.decompose()

    def _read_file(self, xml_path: str) -> str:
        if not os.path.exists(xml_path):
            raise FileNotFoundError(f"XML file not found: {xml_path}")

        with open(xml_path, "r", encoding="utf-8") as f:
            return f.read()

    def _build_soup(self, xml_content: str, fallback: bool = False) -> BeautifulSoup:
        if not fallback:
            return BeautifulSoup(xml_content, "xml")

        try:
            return BeautifulSoup(xml_content, "xml")
        except Exception:
            return BeautifulSoup(xml_content, "html.parser")

    def _is_leaf(self, node) -> bool:
        return not node.find_all()

    def _append_if_text(self, elem, target: list[str]) -> None:
        text = elem.get_text(strip=True)
        if text:
            target.append(text)

    def extract_tables(self, xml_path: str) -> list[str]:
        soup = self._build_soup(self._read_file(xml_path))
        self._strip_boilerplate(soup)

        flat_data: list[str] = []

        for para_elem in soup.find_all("Paragraph"):
            self._append_if_text(para_elem, flat_data)

        for table_elem in soup.find_all("Table"):
            for row_elem in table_elem.find_all("Row"):
                for col_elem in row_elem.find_all("Col"):
                    self._append_if_text(col_elem, flat_data)

        return flat_data

    def _extract_values(self, obj, valid_set: set[str]) -> None:
        if isinstance(obj, dict):
            for v in obj.values():
                self._extract_values(v, valid_set)
        elif isinstance(obj, list):
            for v in obj:
                self._extract_values(v, valid_set)
        else:
            if obj is not None:
                valid_set.add(str(obj).replace("\r", "").strip())

    def _clean(self, s) -> str:
        return "".join(str(s).split())

    def cleaned_values(self, valid_data: dict | list) -> set[str]:
        """Normaliza `valid_data` a las claves con las que compara `matches`."""
        valid_set: set[str] = set()
        self._extract_values(valid_data, valid_set)

        return {self._clean(v) for v in valid_set}

    def matches(self, text: str, valid_cleaned: set[str]) -> bool:
        """Único criterio de correspondencia texto-XML ↔ valor del pipeline.

        Es público porque `ChangeScopeService` tiene que emparejar con
        exactamente el mismo rasero que usará después `prune_xml`: con un
        criterio propio acabaría descartando valores que la poda sí habría
        conservado, decidiendo por encima del pipeline.
        """
        cleaned = self._clean(text).lower()

        for v in valid_cleaned:
            v_lower = v.lower()
            if cleaned == v_lower:
                return True
            if len(cleaned) >= 4 and len(v_lower) >= 4 and (cleaned in v_lower or v_lower in cleaned):
                return True

        return False

    def prune_xml(self, xml_path: str, valid_data: dict | list) -> str:
        print(valid_data)
        soup = self._build_soup(self._read_file(xml_path), fallback=True)
        self._strip_boilerplate(soup)

        valid_cleaned = self.cleaned_values(valid_data)

        # 1. Poda los nodos hoja con texto que no está en los datos válidos
        for node in soup.find_all():
            if self._is_leaf(node):
                text = node.get_text()
                if self._clean(text) and not self.matches(text, valid_cleaned):
                    node.decompose()

        # 2. Limpia recursivamente los nodos que quedaron vacíos
        changed = True
        while changed:
            changed = False
            for node in soup.find_all():
                if self._is_leaf(node) and not self._clean(node.get_text()):
                    if node.name != "Document":
                        node.decompose()
                        changed = True

        output_path = xml_path.replace(".xml", f"_pruned_{uuid.uuid4().hex[:6]}.xml")
        with open(output_path, "w", encoding="utf-8") as f:
            print(soup.prettify())
            f.write(soup.prettify())

        return output_path

