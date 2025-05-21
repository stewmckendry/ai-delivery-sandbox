class DummyTool:
    def __init__(self, name):
        self.name = name

    def run(self, input_data):
        return f"{self.name} processed input: {input_data}"


TOOL_CATALOG = {
    "intent_classifier": DummyTool("intent_classifier"),
    "schema_loader": DummyTool("schema_loader"),
    "section_writer": DummyTool("section_writer"),
}