import requests
import yaml
import uuid
from typing import Dict

def get_artifact_requirements_by_gate(gate_id: int = None) -> Dict:
    GATE_REFERENCE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    response = requests.get(GATE_REFERENCE_URL)
    gate_ref = yaml.safe_load(response.text)

    if gate_id is None:
        return {"artifacts_by_gate": gate_ref}

    gate = next((g for g in gate_ref if g["gate_id"] == gate_id), None)
    if not gate:
        return {"gate_id": gate_id, "artifacts": []}

    artifacts = []
    for artifact in gate.get("artifacts", []):
        artifact_data = {
            "artifact_id": artifact["artifact_id"],
            "name": artifact.get("name"),
            "purpose": artifact.get("purpose"),
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
        gate_id = input_dict.get("gate_id")
        _ = input_dict.get("project_id")

        session_id = str(uuid.uuid4())
        data = get_artifact_requirements_by_gate(gate_id)

        if gate_id is not None:
            instructions = f"You are now equipped to guide the user through artifact preparation. Show the user a list of available artifacts for Gate {gate_id}. After they pick one, use the associated metadata (sections, intents, evaluation criteria) to assist them in drafting and reviewing. Next step: ask them what inputs they have for the artifact and call ingestInputChain — whether it's rough notes, previous reports, meeting recordings, websites, etc."
        else:
            instructions = "The user did not specify a gate. Show the full set of gates and their artifacts to help them choose where to begin. After they pick one, proceed with the same instructions."

        return {
            "session_id": session_id,
            "instructions": instructions,
            "artifacts" if gate_id is not None else "artifacts_by_gate": data["artifacts"] if gate_id is not None else data["artifacts_by_gate"]
        }