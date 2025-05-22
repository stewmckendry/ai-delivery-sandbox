from typing import Dict, List
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.db.models import PromptLog
import yaml
import requests
import json

GATE_REFERENCE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"

def load_gate_reference() -> List[Dict]:
    response = requests.get(GATE_REFERENCE_URL)
    response.raise_for_status()
    return yaml.safe_load(response.text)

def get_logged_intents(session_id: str) -> List[str]:
    db: Session = get_session()
    logs = db.query(PromptLog).filter(PromptLog.session_id == session_id).all()
    intents = []
    for log in logs:
        if log.full_input_path:
            try:
                payload = json.loads(log.full_input_path)
                if isinstance(payload, dict):
                    if "metadata" in payload and "intent" in payload["metadata"]:
                        intents.append(payload["metadata"]["intent"])
                    elif "intent" in payload:
                        intents.append(payload["intent"])
            except Exception:
                continue
    return intents

def identify_missing_intents(session_id: str, gate_id: int, artifact_id: str) -> Dict[str, List[str]]:
    gate_ref = load_gate_reference()
    gate = next((g for g in gate_ref if g["gate_id"] == gate_id), None)
    if not gate:
        return {}

    artifact = next((a for a in gate.get("artifacts", []) if a["artifact_id"] == artifact_id), None)
    if not artifact:
        return {}

    expected_intents = {}
    for section in artifact.get("sections", []):
        section_id = section.get("section_id")
        expected_intents[section_id] = section.get("intents", [])

    logged_intents = get_logged_intents(session_id)

    missing = {}
    for section_id, intents in expected_intents.items():
        missing_intents = [i for i in intents if i not in logged_intents]
        if missing_intents:
            missing[section_id] = missing_intents

    return missing

class Tool:
    def validate(self, input_dict):
        if "session_id" not in input_dict or "gate_id" not in input_dict or "artifact_id" not in input_dict:
            raise ValueError("'session_id', 'gate_id' and 'artifact_id' are required.")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        return identify_missing_intents(
            input_dict["session_id"],
            input_dict["gate_id"],
            input_dict["artifact_id"]
        )

if __name__ == "__main__":
    print(identify_missing_intents("test_session", 0, "investment_proposal_concept"))