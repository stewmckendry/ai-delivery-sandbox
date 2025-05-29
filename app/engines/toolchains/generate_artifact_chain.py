import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.project_profile_engine import ProjectProfileEngine
from app.engines.toolchains.global_context_chain import GlobalContextEngine
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.tools.tool_wrappers.memory_retrieve import Tool as MemoryTool
from app.tools.utils.section_helpers import plan_sections
from app.engines.memory_sync import log_tool_usage

logger = logging.getLogger(__name__)

class GenerateArtifactChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = MemoryTool()
        self.section_chain = GenerateSectionChain()
        self.profile_engine = ProjectProfileEngine()
        self.global_context_engine = GlobalContextEngine()

    def run(self, inputs):
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact_id")
        gate_id = inputs.get("gate_id")
        project_id = inputs.get("project_id")

        logger.info("[Step 1] Load section definitions")
        section_definitions = plan_sections(gate_id, artifact_id)
        log_tool_usage("section_helpers", "planned section definitions", section_definitions, session_id, user_id, inputs)

        logger.info("[Step 2] Fetch + summarize global context")
        context_data = self.global_context_engine.fetch_logged_global_context(project_id, session_id)
        global_context_summary = self.global_context_engine.summarize_global_context(context_data)
        global_context = {
            "global_context": context_data,
            "global_context_summary": global_context_summary,
        }
        log_tool_usage("global_context_chain", "fetched global context", context_data, session_id, user_id, inputs)
        log_tool_usage("global_context_chain", "summarized global context", global_context_summary, session_id, user_id, inputs)
        
        logger.info("[Step 3] Generate each section")
        all_sections_output = []

        for section in section_definitions:
            section_id = section["section_id"]
            inputs["section_id"] = section_id
            try:
                result = self.section_chain.run(inputs=inputs, global_context=context_data)
                draft = result["final_output"]["raw_draft"]
                all_sections_output.append({"section_id": section_id, "draft": draft})
                logger.info(f"[Step 3.x] Generated section: {section_id} complete")
                log_tool_usage("generate_section_chain", f"generated section draft for {section_id}", draft, session_id, user_id, inputs)
            except Exception as e:
                logger.error(f"[Step 3.x] Error generating section {section_id}: {e}")
                all_sections_output.append({
                    "section_id": section_id,
                    "error": str(e),
                    "draft": ""
                })

        return {"sections": all_sections_output, "summary": global_context_summary}