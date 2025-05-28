from typing import Dict, List
import requests
import yaml
import json
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt

def get_logged_intents(session_id: str) -> List[str]:
    from app.db.models.PromptLog import PromptLog
    from app.db.database import SessionLocal
    with SessionLocal() as session:
        logs = session.query(PromptLog).filter(PromptLog.session_id == session_id).all()
        return [log.input_summary or "" for log in logs if log.input_summary]

def identify_missing_intents(session_id: str, gate_id: int, artifact_id: str) -> Dict:
    with open("project/reference/gate_reference_v2.yaml") as f:
        gate_reference = yaml.safe_load(f)

    expected_intents = gate_reference[str(gate_id)]["artifacts"][artifact_id]["sections"]

    prompt_data = {
        "intents": expected_intents,
        "logged_texts": get_logged_intents(session_id)
    }
    prompt = get_prompt("input_checker_prompts.yaml", "intent_coverage")
    user_prompt = prompt["user"].replace("{{expected_intents}}", json.dumps(expected_intents)).replace("{{logged_texts}}", "\n".join(prompt_data["logged_texts"]))
    return json.loads(chat_completion_request(prompt["system"], user_prompt))

class Tool:
    def validate(self, input_dict):
        if "session_id" not in input_dict or "gate_id" not in input_dict or "artifact_id" not in input_dict:
            raise ValueError("'session_id', 'gate_id' and 'artifact_id' are required.")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        return identify_missing_intents(
            session_id=input_dict["session_id"],
            gate_id=input_dict["gate_id"],
            artifact_id=input_dict["artifact_id"]
        )

