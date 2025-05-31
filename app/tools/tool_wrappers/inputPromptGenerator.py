import requests
import yaml
from typing import List, Dict, Optional

def load_yaml(path_or_url: str) -> dict:
    if path_or_url.startswith("http"):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return yaml.safe_load(response.text)
    else:
        with open(path_or_url, 'r') as file:
            return yaml.safe_load(file)

def generate_question_map(gate_id: int, artifact_id: str) -> List[Dict]:
    GATE_REFERENCE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    gate_ref = load_yaml(GATE_REFERENCE_URL)
    prompts = []

    gate = next((g for g in gate_ref if g["gate_id"] == gate_id), None)
    if not gate:
        return prompts

    artifact = next((a for a in gate.get("artifacts", []) if a["artifact_id"] == artifact_id), None)
    if not artifact:
        return prompts

    for section in artifact.get("sections", []):
        for intent in section.get("intents", []):
            prompt = {
                "question": intent,
                "input_type": "text",
                "answer": None,
                "metadata": {
                    "gate": gate_id,
                    "artifact": artifact_id,
                    "section": section["section_id"],
                    "intent": intent
                },
                "hints": artifact.get("evaluation_criteria", []),
                "required": section.get("mandatory", False),
                "artifact_name": artifact.get("name"),
                "artifact_purpose": artifact.get("purpose"),
                "artifact_template": artifact.get("template_path"),
                "artifact_exemplar": artifact.get("exemplar_path"),
                "maturity": artifact.get("maturity"),
                "notes": artifact.get("notes")
            }
            prompts.append(prompt)

    return prompts

class Tool:

    def run_tool(self, input_dict):
        gate_id = input_dict["gate_id"]
        artifact_id = input_dict["artifact_id"]
        return generate_question_map(gate_id, artifact_id)
