import logging
from typing import Dict, Any

from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain
from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.memory_sync import load_project_profile

logger = logging.getLogger(__name__)

class PlannerOrchestrator:
    def __init__(self, mode: str = "live"):
        self.mode = mode

    def run(self, intent: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Planner starting for intent: {intent}")
        project_id = inputs.get("project_id")
        if project_id:
            try:
                profile = load_project_profile(project_id)
                inputs["project_profile"] = profile
                logger.info(f"Loaded project profile for project_id: {project_id}")
            except Exception as e:
                logger.warning(f"Project profile load failed: {e}")

        if intent == "generate_section":
            return GenerateSectionChain().run(inputs)
        elif intent == "assemble_artifact":
            return AssembleArtifactChain().run(inputs)
        elif intent == "ingest_input":
            return IngestInputChain().run(inputs)

        raise ValueError(f"No toolchain defined for intent: {intent}")