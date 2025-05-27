import logging
import uuid
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain
from app.tools.utils.section_helpers import plan_sections, summarize_previous
from app.engines.memory_sync import log_tool_usage

logger = logging.getLogger(__name__)

class GenerateFullArtifactChain:
    def __init__(self):
        self.section_chain = GenerateSectionChain()
        self.assembler = AssembleArtifactChain()

    def run(self, artifact_id, gate_id, project_id, user_id=None):
        session_id = str(uuid.uuid4())
        logger.info(f"[START] Full artifact chain for {artifact_id} - gate {gate_id}")

        sections = plan_sections(gate_id, artifact_id)
        log_tool_usage("plan_sections", "planned section list", sections, session_id, user_id, {"gate_id": gate_id, "artifact_id": artifact_id})

        for i, section in enumerate(sections):
            context_summary = summarize_previous(sections[:i])
            inputs = {
                "artifact": artifact_id,
                "gate_id": gate_id,
                "section": section["section_id"],
                "project_id": project_id,
                "context_summary": context_summary,
                "session_id": session_id,
                "user_id": user_id
            }
            result = self.section_chain.run(inputs)
            log_tool_usage("generate_section_chain", "section output", result, session_id, user_id, inputs)

        assemble_inputs = {
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "project_id": project_id
        }
        assembled = self.assembler.run(assemble_inputs)
        log_tool_usage("assemble_artifact_chain", "assembled document", assembled, session_id, user_id, assemble_inputs)

        return {"session_id": session_id, "drive_link": assembled.get("final_output", {}).get("drive_url")}