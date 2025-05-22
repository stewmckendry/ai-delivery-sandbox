# app/tools/tool_wrappers/inputPromptGenerator.py

from typing import List, Dict, Optional
import yaml
import os
import requests

TRIAGE_MAP_PATH = "project/reference/triage_map_policygpt.yaml"
GATE_REFERENCE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"


def load_yaml(path_or_url: str) -> dict:
    if path_or_url.startswith("http"):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return yaml.safe_load(response.text)
    else:
        with open(path_or_url, 'r') as file:
            return yaml.safe_load(file)


def generate_input_prompts(gate_id: int, artifact_id: str, section_id: Optional[str] = None) -> List[Dict]:
    gate_ref = load_yaml(GATE_REFERENCE_URL)
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


class Tool:
    def validate(self, input_dict):
        if "gate_id" not in input_dict or "artifact_id" not in input_dict:
            raise ValueError("Both 'gate_id' and 'artifact_id' are required.")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        gate_id = input_dict["gate_id"]
        artifact_id = input_dict["artifact_id"]
        section_id = input_dict.get("section_id")
        return generate_input_prompts(gate_id, artifact_id, section_id)


if __name__ == "__main__":
    prompts = generate_input_prompts(0, "investment_proposal_concept")
    from pprint import pprint
    pprint(prompts)