from typing import List
from pydantic import BaseModel
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from app.engines.memory_sync import log_tool_usage
import yaml
import os

GATE_REF_PATH = os.path.join("project", "reference", "gate_reference_v2.yaml")

def get_gate_section_order(gate_id: str) -> List[str]:
    with open(GATE_REF_PATH, "r") as f:
        gates = yaml.safe_load(f)
    gate_data = next((g for g in gates if str(g.get("gate_id")) == gate_id), {})
    return [s.get("section_id") for s in gate_data.get("sections", [])]

class InputSchema(BaseModel):
    artifact_id: str
    gate_id: str

class OutputSchema(BaseModel):
    ordered_sections: List[dict]

class Tool:
    def validate(self, input_dict):
        input_data = InputSchema(**input_dict)  # Validates via Pydantic
        return input_data

    def run_tool(self, input_dict):
        input_data = self.validate(input_dict)
        session = get_session()
        sections = session.query(ArtifactSection).filter_by(
            artifact_id=input_data.artifact_id,
            gate_id=input_data.gate_id
        ).all()

        section_map = {s.section_id: s for s in sections}
        ordered_ids = get_gate_section_order(input_data.gate_id)

        ordered_sections = []
        for sid in ordered_ids:
            section = section_map.get(sid)
            if section:
                ordered_sections.append({
                    "section_id": section.section_id,
                    "text": section.text,
                    "status": section.status,
                    "timestamp": section.timestamp.isoformat()
                })

        return OutputSchema(ordered_sections=ordered_sections).dict()