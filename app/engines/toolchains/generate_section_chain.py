from app.tools.tool_registry import registry

class GenerateSectionChain:
    def __init__(self):
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")
        self.web_search_tool = registry.get_tool("webSearch")

    def run(self, inputs: dict):
        print("[Step 1] Retrieving memory")
        memory_results = self.memory_tool.run_tool(inputs)

        print("[Step 2] External search")
        web_results = self.web_search_tool.run_tool(inputs)

        memory_wrapped = {"memory": []}

        if memory_results:
            memory_wrapped["memory"].extend(memory_results)

        if web_results:
            memory_wrapped["memory"].extend(web_results)

        draft = self.synth_tool.run_tool({**inputs, **memory_wrapped})
        final = self.refine_tool.run_tool({**inputs, "draft": draft})
        return final