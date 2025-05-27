import requests
import tiktoken
import logging

logger = logging.getLogger(__name__)

def plan_sections(gate_id):
    url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
    response = requests.get(url)
    if not response.ok:
        logger.error(f"Failed to fetch gate reference: {response.status_code}")
        return []

    import yaml
    gates = yaml.safe_load(response.text)
    gate = next((g for g in gates if g['gate_id'] == gate_id), None)
    if not gate:
        logger.warning(f"Gate ID {gate_id} not found in reference")
        return []

    return gate.get("sections", [])

def summarize_previous(sections):
    all_texts = "\n\n".join([s.get("text", "") for s in sections if s.get("text")])
    if get_token_count(all_texts) > 2000:
        return all_texts[:3000] + "... (truncated summary)"
    return all_texts

def get_token_count(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text or ""))