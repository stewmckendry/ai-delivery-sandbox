# app/tools/tool_wrappers/inputPromptGenerator.py

from typing import List, Dict, Optional
import yaml
from app.tools.tool_wrappers import ToolWrapper
import os

TRIAGE_MAP_PATH = "project/reference/triage_map_policygpt.yaml"
GATE_REFERENCE_PATH = "project/reference/gate_reference_v2.yaml"


def load_yaml(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def generate_input_prompts(gate_id: int, artifact_id: str, section_id: Optional[str] = None) -> List[Dict]:
    gate_ref = load_yaml(GATE_REFERENCE_PATH)
    triage_map = load_yaml(TRIAGE_MAP_PATH)
    prompts = []

    gate = next((g for g in gate_ref if g["gate_id"] == gate_id), None)
    if not gate:
        return prompts

    artifact = next((a for a in gate.get("artifacts", []) if a["artifact_id"] == artifact_id), None)
    if not artifact:
        return prompts

    sections = artifact.get("sections", [])
    section_targets = [s for s in sections if section_id is None or s["section_id"] == section_id]

    for section in section_targets:
        intents = triage_map.get(section["section_id"], {}).get("intents", [])
        for intent in intents:
            triage = triage_map.get(intent, {})
            question = triage.get("question", f"Please provide input for {intent}.")
            input_type = triage.get("input_type", "text")
            hints = triage.get("hints", [])

            prompt = {
                "question": question,
                "input_type": input_type,
                "answer": None,
                "metadata": {
                    "gate": gate_id,
                    "artifact": artifact_id,
                    "section": section["section_id"],
                    "intent": intent
                },
                "hints": hints,
                "required": True
            }
            prompts.append(prompt)

    return prompts


class InputPromptGenerator(ToolWrapper):
    tool_name = "inputPromptGenerator"
    description = "Generate structured prompts for a given gate, artifact, and section"
    input_schema = {
        "type": "object",
        "properties": {
            "gate_id": {"type": "integer"},
            "artifact_id": {"type": "string"},
            "section_id": {"type": ["string", "null"]}
        },
        "required": ["gate_id", "artifact_id"]
    }

    def run(self, gate_id: int, artifact_id: str, section_id: Optional[str] = None) -> List[Dict]:
        return generate_input_prompts(gate_id, artifact_id, section_id)


if __name__ == "__main__":
    prompts = generate_input_prompts(0, "investment_proposal_concept")
    from pprint import pprint
    pprint(prompts)