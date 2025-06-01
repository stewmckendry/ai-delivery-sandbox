import requests
import yaml
from typing import Dict, List

def get_artifact_requirements_by_gate(gate_id: int) -> Dict:
    GATE_REFERENCE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    response = requests.get(GATE_REFERENCE_URL)
    gate_ref = yaml.safe_load(response.text)

    gate = next((g for g in gate_ref if g["gate_id"] == gate_id), None)
    if not gate:
        return {"gate_id": gate_id, "artifacts": []}

    artifacts = []
    for artifact in gate.get("artifacts", []):
        artifact_data = {
            "artifact_id": artifact["artifact_id"],
            "name": artifact.get("name"),
            "purpose": artifact.get("purpose"),
            "maturity": artifact.get("maturity"),
            "notes": artifact.get("notes"),
            "evaluation_criteria": artifact.get("evaluation_criteria", []),
            "sections": []
        }

        for section in artifact.get("sections", []):
            artifact_data["sections"].append({
                "section_id": section.get("section_id"),
                "name": section.get("name"),
                "mandatory": section.get("mandatory", False),
                "intents": section.get("intents", [])
            })

        artifacts.append(artifact_data)

    return {
        "gate_id": gate_id,
        "artifacts": artifacts
    }

class Tool:

    def run_tool(self, input_dict):
        gate_id = input_dict["gate_id"]
        return get_artifact_requirements_by_gate(gate_id)
