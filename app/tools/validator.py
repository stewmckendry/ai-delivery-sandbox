import yaml
import requests
from typing import Set

SYMPTOM_YAML_PATHS = [
    "reference/symptoms_physical.yaml",
    "reference/symptoms_emotional.yaml",
    "reference/symptoms_sleep.yaml",
    "reference/symptoms_red_flag.yaml",
]

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox"
BRANCH = "sandbox-silver-tiger"

def load_known_symptom_ids() -> Set[str]:
    """Fetch all known symptom IDs from reference YAMLs in GitHub."""
    ids = set()
    for path in SYMPTOM_YAML_PATHS:
        url = f"{GITHUB_RAW_BASE}/{BRANCH}/{path}"
        response = requests.get(url)
        if response.status_code == 200:
            data = yaml.safe_load(response.text)
            for item in data.get("symptoms", []):
                ids.add(item["id"])
    return ids

def validate_symptom_ids(input_ids: Set[str]) -> bool:
    """Check if all input symptom IDs are valid."""
    known_ids = load_known_symptom_ids()
    invalid_ids = input_ids - known_ids
    if invalid_ids:
        raise ValueError(f"Invalid symptom IDs found: {sorted(invalid_ids)}")
    return True