import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.project_profile_engine import ProjectProfileEngine
from app.engines.toolchains.global_context_chain import GlobalContextEngine
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.tools.tool_wrappers.memory_retrieve import Tool as MemoryTool
from app.tools.utils.section_helpers import load_section_definitions

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

        logger.info("[Step 1] Load project profile")
        project_profile = self.profile_engine.load_profile(project_id)
        inputs["project_profile"] = project_profile

        logger.info("[Step 2] Retrieve memory")
        memory = self.memory_tool.run_tool({**inputs, "project_profile": project_profile})

        logger.info("[Step 3] Load section definitions")
        section_definitions = load_section_definitions(gate_id, artifact_id)

        logger.info("[Step 4] Fetch + summarize global context")
        context_data = self.global_context_engine.fetch_logged_global_context(project_id, session_id)
        global_context_summary = self.global_context_engine.summarize_global_context(context_data)

        logger.info("[Step 5] Generate each section")
        all_sections_output = []

        for section in section_definitions:
            section_id = section["section_id"]
            section_inputs = {
                **inputs,
                "artifact": artifact_id,
                "section": section_id,
                "memory": memory,
                "context_summary": "",
                "global_context_summary": global_context_summary,
            }
            result = self.section_chain.run(section_inputs, global_context=context_data)
            draft = result["final_output"]["raw_draft"]
            all_sections_output.append({"section_id": section_id, "draft": draft})

        return {"sections": all_sections_output, "summary": global_context_summary}