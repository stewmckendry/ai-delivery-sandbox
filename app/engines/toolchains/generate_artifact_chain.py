import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain
from app.engines.project_profile_engine import ProjectProfileEngine
from app.reference.gate_reference_v2 import gate_reference

logger = logging.getLogger(__name__)

class GenerateArtifactChain:
    def __init__(self):
        registry = ToolRegistry()
        self.section_chain = GenerateSectionChain()
        self.assembler = AssembleArtifactChain()
        self.project_profile_engine = ProjectProfileEngine()

    def run(self, inputs):
        gate_id = int(inputs["gate_id"])
        artifact_id = inputs["artifact"]
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        project_id = inputs.get("project_id")

        # Load profile
        profile = self.project_profile_engine.load_profile(project_id)

        # Prepare section metadata
        artifact = next(a for a in gate_reference[gate_id]["artifacts"] if a["artifact_id"] == artifact_id)
        sections = artifact["sections"]

        # Retrieve memory
        memory = ToolRegistry().get_tool("memory_retrieve").run_tool({
            "session_id": session_id,
            "user_id": user_id,
            "project_profile": profile,
            "gate_id": gate_id,
            "artifact": artifact_id,
            "project_id": project_id
        })

        # Generate global context
        global_context = self.section_chain.generate_global_context(
            inputs, profile, memory, session_id, user_id
        )

        # Iterate through each section
        section_outputs = []
        prior_summaries = []
        for section in sections:
            section_id = section["section_id"]
            section_inputs = {
                **inputs,
                "section": section_id,
                "project_profile": profile,
                "prior_sections_summary": "\n\n".join(prior_summaries)
            }
            output = self.section_chain.run(section_inputs, global_context=global_context)
            final_text = output["final_output"]["raw_draft"]
            prior_summaries.append(final_text)
            section_outputs.append({"section_id": section_id, "text": final_text})

        # Assemble full artifact
        return self.assembler.run({
            "artifact": artifact_id,
            "gate_id": gate_id,
            "project_id": project_id,
            "user_id": user_id,
            "sections": section_outputs
        })