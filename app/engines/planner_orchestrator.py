import logging
from typing import Dict, Any

from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain

logger = logging.getLogger(__name__)

class PlannerOrchestrator:
    def __init__(self, mode: str = "live"):
        self.mode = mode

    def run(self, intent: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Planner starting for intent: {intent}")
        if intent == "generate_section":
            return GenerateSectionChain().run(inputs)
        elif intent == "assemble_artifact":
            return AssembleArtifactChain().run(inputs)
        raise ValueError(f"No toolchain defined for intent: {intent}")