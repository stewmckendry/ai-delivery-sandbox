import logging
import uuid
import os
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage
from jinja2 import Template
from app.engines.project_profile_engine import ProjectProfileEngine

logger = logging.getLogger(__name__)

class GenerateSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")

    def run(self, inputs, global_context=None):
        trace = []
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact")
        section_id = inputs.get('section')
        gate_id = inputs.get("gate_id", "0")
        project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

        #load project profile if available
        if project_id:
            profile_engine = ProjectProfileEngine()
            project_profile = profile_engine.load_profile(project_id)
        else:
            project_profile = {}
        inputs["project_profile"] = project_profile

        context_summary = inputs.get("context_summary", "")
        log_tool_usage("context_summary", "context summary input", context_summary, session_id, user_id, inputs)

        memory_input = {**inputs}
        memory_input["project_profile"] = project_profile

        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        if global_context is None:
            global_context = self.generate_global_context(inputs, project_profile, memory, session_id, user_id)
            logger.info("[Optional Step] Generated global context from web search, corpus, and alignment")
        
        structured_inputs = {
            "memory": memory,
            "web_search": global_context["web_search"],
            "corpus_answer": global_context["corpus_answer"],
            "alignment_results": global_context["alignment_results"],
            "context_summary": context_summary
        }

        draft = self.synth_tool.run_tool({**inputs, **structured_inputs})
        log_tool_usage("section_synthesizer", "generated draft", draft, session_id, user_id, inputs)
        trace.append({"tool": "section_synthesizer", "output": draft})
        logger.info("[Step 6] section_synthesizer complete")

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        log_tool_usage("section_refiner", "refined draft", refined, session_id, user_id, inputs)
        trace.append({"tool": "section_refiner", "output": refined})
        logger.info("[Step 7] section_refiner complete")

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
        logger.info("[Step 8] Saved to ArtifactSection and ReasoningTrace")

        return {"final_output": refined, "trace": trace, "save_result": save_result}