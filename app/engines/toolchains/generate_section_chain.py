from app.engine_base import ToolChain
from app.registry import registry

class GenerateSectionChain(ToolChain):
    def __init__(self):
        super().__init__()
        self.retriever = registry.get_tool("memoryRetrieve")
        self.metadata_loader = registry.get_tool("loadSectionMetadata")
        self.synthesizer = registry.get_tool("sectionSynthesizer")
        self.refiner = registry.get_tool("sectionRefiner")
        self.prompt_generator = registry.get_tool("queryPromptGenerator")
        self.formatter = registry.get_tool("formatSection")
        self.uploader = registry.get_tool("uploadTextInput")
        self.committer = registry.get_tool("storeToDrive")