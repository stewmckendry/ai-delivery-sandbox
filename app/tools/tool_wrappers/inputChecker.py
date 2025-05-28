from typing import Dict, List
import requests
import yaml
import json
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt

def get_logged_intents(session_id: str) -> List[str]:
    # Stubbed logs (replace with real DB fetch later)
    return [
        "We need to improve service delivery across departments.",
        "This will enhance citizen trust in digital platforms."
    ]

def identify_missing_intents(session_id: str, gate_id: int, artifact_id: str) -> Dict:
    with open("project/reference/gate_reference_v2.yaml") as f:
        gate_reference = yaml.safe_load(f)

    expected_intents = gate_reference[str(gate_id)]["expected_intents"]

    prompt_data = {
        "intents": expected_intents,
        "logged_texts": get_logged_intents(session_id)
    }
    prompt = get_prompt("input_checker_prompts.yaml", "intent_coverage")
    user_prompt = prompt["user"].replace("{{expected_intents}}", json.dumps(expected_intents)).replace("{{logged_texts}}", "\n".join(prompt_data["logged_texts"]))
    return json.loads(chat_completion_request(prompt["system"], user_prompt))