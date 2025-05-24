from typing import List
from pydantic import BaseModel, ValidationError
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
import yaml
import requests
from sqlalchemy import desc
import logging

logger = logging.getLogger(__name__)
GATE_REF_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"

def get_gate_section_order(gate_id: str, artifact_id: str) -> List[str]:
    response = requests.get(GATE_REF_URL)
    gates = yaml.safe_load(response.text)
    for gate in gates:
        if str(gate.get("gate_id")) == gate_id:
            for artifact in gate.get("artifacts", []):
                if artifact.get("artifact_id") == artifact_id:
                    return [s.get("section_id") for s in artifact.get("sections", [])]
    return []

class InputSchema(BaseModel):
    artifact_id: str
    gate_id: str

class OutputSchema(BaseModel):
    artifact_name: str
    ordered_sections: List[dict]

class Tool:
    def validate(self, input_dict):
        logger.info(f"Validating input: {input_dict}")
        try:
            return InputSchema(**input_dict)
        except ValidationError as e:
            logger.error(f"Input validation failed: {e}")
            raise ValueError(f"Invalid input: {e}")

    def run_tool(self, input_dict):
        logger.info(f"Running tool with input: {input_dict}")
        input_data = self.validate(input_dict)
        logger.info(f"Validated input_data: {input_data}")
        logger.info(f"Type of input_data: {type(input_data)}")
        session = get_session()

        logger.info(f"Fetching gate reference from {GATE_REF_URL}")
        response = requests.get(GATE_REF_URL)
        logger.info(f"Gate reference status: {response.status_code}")
        gates = yaml.safe_load(response.text)

        artifact_name = ""
        section_ids = []
        logger.info(f"Parsing gates for artifact_id={input_data.artifact_id} and gate_id={input_data.gate_id}")
        for gate in gates:
            logger.debug(f"Gate found: {gate.get('gate_id')}")
            if str(gate.get("gate_id")) == input_data.gate_id:
                for artifact in gate.get("artifacts", []):
                    logger.debug(f"Checking artifact_id={artifact.get('artifact_id')}")
                    if artifact.get("artifact_id") == input_data.artifact_id:
                        artifact_name = artifact.get("name")
                        section_ids = [s.get("section_id") for s in artifact.get("sections", [])]
                        break

        section_map = {}
        for sid in section_ids:
            latest = session.query(ArtifactSection).filter_by(
                artifact_id=input_data.artifact_id,
                gate_id=input_data.gate_id,
                section_id=sid,
                status='draft'
            ).order_by(desc(ArtifactSection.timestamp)).first()
            if latest:
                section_map[sid] = latest

        ordered_sections = []
        for sid in section_ids:
            section = section_map.get(sid)
            if section:
                ordered_sections.append({
                    "section_id": section.section_id,
                    "text": section.text,
                    "status": section.status,
                    "timestamp": section.timestamp.isoformat()
                })

        return OutputSchema(artifact_name=artifact_name, ordered_sections=ordered_sections).dict()