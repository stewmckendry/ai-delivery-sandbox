import logging
import uuid
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage

logger = logging.getLogger(__name__)

class GenerateSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")
        self.web_search_tool = registry.get_tool("webSearch")

    def run(self, inputs):
        trace = []
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact")
        section_id = f"{artifact_id}_{inputs.get('section')}"
        gate_id = inputs.get("gate_id", "0")
        project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

        memory_input = {**inputs}
        if "project_profile" in inputs:
            memory_input["project_profile"] = inputs["project_profile"]

        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        search_results = self.web_search_tool.run_tool({
            "query": f"{inputs.get('artifact')} - {inputs.get('section')}",
            "search_type": "general",
            "context": {"project_profile": inputs.get("project_profile", {})}
        })
        log_tool_usage("web_search", "external scan", search_results, session_id, user_id, inputs)
        trace.append({"tool": "web_search", "output": search_results})
        logger.info("[Step 2] web_search complete")

        memory_wrapped = {"memory": memory + search_results}

        draft = self.synth_tool.run_tool({**inputs, **memory_wrapped})
        log_tool_usage("section_synthesizer", "generated draft", draft, session_id, user_id, inputs)
        trace.append({"tool": "section_synthesizer", "output": draft})
        logger.info("[Step 3] section_synthesizer complete")

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        log_tool_usage("section_refiner", "refined draft", refined, session_id, user_id, inputs)
        trace.append({"tool": "section_refiner", "output": refined})
        logger.info("[Step 4] section_refiner complete")

        save_result = save_artifact_and_trace(
            section_id=section_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            text=refined["raw_draft"],
            sources=draft.get("prompt_used"),
            tool_outputs=trace,
            user_id=user_id,
            project_id=project_id
        )
        logger.info("[Step 5] Saved to ArtifactSection and ReasoningTrace")

        return {"final_output": refined, "trace": trace, "save_result": save_result}