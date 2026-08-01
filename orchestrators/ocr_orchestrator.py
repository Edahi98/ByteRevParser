from orchestrators.xml_orchestrator import XmlOrchestrator
from services.markdown_service import MarkdownService
from services.nuextract_service import NuExtractService
from services.pipeline_service import PipelineService
from services.redactor_service import RedactorService
from services.tsubasa_service import TsubasaService
from services.xml_service import XmlService


class OcrOrchestrator:
    """Orquesta el flujo completo: documento + pipeline -> XML -> Tsubasa -> resultado final."""

    def __init__(self):
        self.xml_orchestrator = XmlOrchestrator()
        self.xml_service = XmlService()
        self.markdown_service = MarkdownService()
        self.pipeline_service = PipelineService()
        self.tsubasa_service = TsubasaService()
        self.nuextract_service = NuExtractService()
        self.redactor_service = RedactorService()

    def run(self, input_path: str, pipeline: dict, schema: dict) -> dict:
        xml_path = self.xml_orchestrator.get_xml(input_path)

        extracted_data = self.xml_service.extract_tables(xml_path)
        pipeline = self.pipeline_service.replace_data(pipeline, extracted_data)

        result_data = self.tsubasa_service.execute(pipeline)

        pruned_path = self.xml_service.prune_xml(xml_path, result_data)
        markdown = self.markdown_service.to_markdown(pruned_path)
        prose = self.redactor_service.redact(markdown)
        return self.nuextract_service.extract(prose, schema)
