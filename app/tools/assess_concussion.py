from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List
import requests
import yaml

router = APIRouter()

SYMPTOM_YAML_URLS = [
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_red_flag.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_physical.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_emotional.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_sleep.yaml",
]

class AssessmentRequest(BaseModel):
    answers: Dict[str, int]  # symptom_id → 0–5 severity rating

@router.post("/assess_concussion", tags=["assessment"])
def assess_concussion(payload: AssessmentRequest):
    known_symptoms = {}
    for url in SYMPTOM_YAML_URLS:
        response = requests.get(url)
        response.raise_for_status()
        yaml_data = yaml.safe_load(response.text)
        for s in yaml_data.get("symptoms", []):
            known_symptoms[s["id"]] = s

    red_flags = []
    high_risk_symptoms = []
    moderate_risk_count = 0

    for sid, rating in payload.answers.items():
        if rating < 1:
            continue
        meta = known_symptoms.get(sid)
        if not meta:
            continue

        tags = meta.get("tool_tags", [])
        if "red_flag" in tags:
            red_flags.append(meta["name"])
        elif meta.get("risk_level") == "high":
            high_risk_symptoms.append(meta["name"])
        elif meta.get("risk_level") == "medium":
            moderate_risk_count += 1

    likely = bool(red_flags or high_risk_symptoms or moderate_risk_count >= 3)
    summary = "This response suggests symptoms consistent with a potential concussion. Please seek clinical evaluation." if likely else "No red flags or high-risk symptom patterns were detected. Monitor closely and consult a provider if symptoms worsen."

    return {
        "concussion_likely": likely,
        "red_flags_present": red_flags,
        "high_risk_symptoms": high_risk_symptoms,
        "moderate_risk_count": moderate_risk_count,
        "summary": summary
    }