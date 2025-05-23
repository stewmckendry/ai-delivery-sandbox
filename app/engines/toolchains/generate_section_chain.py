from app.tools.tool_registry import ToolRegistry

class GenerateSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")

    def run(self, inputs):
        trace = []

        memory = self.memory_tool.run_tool(inputs)
        memory_wrapped = {"memory": memory}
        trace.append({"tool": "memory_retrieve", "output": memory_wrapped})
        print("[Step 1] memory_retrieve complete")

        draft = self.synth_tool.run_tool({**inputs, **memory_wrapped})
        trace.append({"tool": "section_synthesizer", "output": draft})
        print("[Step 2] section_synthesizer complete")

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        trace.append({"tool": "section_refiner", "output": refined})
        print("[Step 3] section_refiner complete")

        return {"final_output": refined, "trace": trace}