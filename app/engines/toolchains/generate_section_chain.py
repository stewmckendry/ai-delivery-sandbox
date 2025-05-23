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
        trace.append({"tool": "memory_retrieve", "output": memory})

        draft = self.synth_tool.run_tool({**inputs, "memory": memory})
        trace.append({"tool": "section_synthesizer", "output": draft})

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        trace.append({"tool": "section_refiner", "output": refined})

        return {"final_output": refined, "trace": trace}