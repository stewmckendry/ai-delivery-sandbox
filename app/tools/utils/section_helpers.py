import requests
import tiktoken
import yaml
import logging

logger = logging.getLogger(__name__)

def plan_sections(gate_id, artifact_id):
    url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    response = requests.get(url)
    if not response.ok:
        logger.error(f"Failed to fetch gate reference: {response.status_code}")
        return []

    gates = yaml.safe_load(response.text)
    gate = next((g for g in gates if str(g['gate_id']) == str(gate_id)), None)
    if not gate:
        logger.warning(f"Gate ID {gate_id} not found in reference")
        return []

    artifact = next((a for a in gate.get('artifacts', []) if a['artifact_id'] == artifact_id), None)
    if not artifact:
        logger.warning(f"Artifact ID {artifact_id} not found in gate {gate_id}")
        return []

    return artifact.get("sections", [])

def summarize_previous(sections):
    all_texts = "\n\n".join([s.get("text", "") for s in sections if s.get("text")])
    if get_token_count(all_texts) > 2000:
        return all_texts[:3000] + "... (truncated summary)"
    return all_texts

def get_token_count(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text or ""))

def load_section_definitions(gate_id, artifact_id):
    url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code

    data = yaml.safe_load(response.text)

    gate = next((g for g in data if str(g["gate_id"]) == str(gate_id)), None)
    if not gate:
        raise ValueError(f"Gate {gate_id} not found")

    artifact = next((a for a in gate["artifacts"] if a["artifact_id"] == artifact_id), None)
    if not artifact:
        raise ValueError(f"Artifact {artifact_id} not found in Gate {gate_id}")

    return artifact.get("sections", [])
