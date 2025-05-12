import yaml
import requests
from pydantic import BaseModel
from typing import Dict, List

SYMPTOM_YAML_PATHS = [
    "reference/symptoms_physical.yaml",
    "reference/symptoms_emotional.yaml",
    "reference/symptoms_sleep.yaml",
    "reference/symptoms_red_flag.yaml"
]

SYMPTOM_YAML_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/"

class SymptomDefinition(BaseModel):
    id: str
    name: str
    tool_tags: List[str] = []
    risk_level: str = ""

def load_symptom_definitions() -> Dict[str, SymptomDefinition]:
    known = {}
    for path in SYMPTOM_YAML_PATHS:
        url = SYMPTOM_YAML_BASE + path
        res = requests.get(url)
        if res.status_code == 200:
            yaml_data = yaml.safe_load(res.text)
            for s in yaml_data.get("symptoms", []):
                known[s["id"]] = SymptomDefinition(
                    id=s["id"],
                    name=s.get("name", ""),
                    tool_tags=s.get("tool_tags", []),
                    risk_level=s.get("risk_level", "")
                )
    return known

def validate_symptom_ids(ids: List[str]):
    known = load_symptom_definitions()
    for sid in ids:
        if sid not in known:
            raise ValueError(f"Invalid symptom ID: {sid}")