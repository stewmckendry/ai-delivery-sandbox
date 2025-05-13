from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import requests
import yaml
from datetime import datetime
from app.db.db_models import ConcussionAssessment, SymptomLog
from app.db.database import SessionLocal

router = APIRouter()

SYMPTOM_YAML_URLS = [
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_red_flag.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_physical.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_emotional.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_sleep.yaml",
]

class AssessmentRequest(BaseModel):
    user_id: str

@router.post("/assess_concussion", tags=["assessment"])
def assess_concussion(payload: AssessmentRequest):
    db = SessionLocal()
    try:
        known_symptoms = {}
        for url in SYMPTOM_YAML_URLS:
            response = requests.get(url)
            response.raise_for_status()
            yaml_data = yaml.safe_load(response.text)
            for s in yaml_data.get("symptoms", []):
                known_symptoms[s["id"]] = s

        logs = db.query(SymptomLog).filter_by(user_id=payload.user_id).all()
        if not logs:
            raise HTTPException(status_code=400, detail="No symptom log found. Complete triage first.")

        symptom_scores = {}
        for entry in logs:
            if entry.symptom_id and entry.score is not None:
                symptom_scores[entry.symptom_id] = entry.score

        red_flags = []
        high_risk_symptoms = []
        moderate_risk_symptoms = []

        for sid, rating in symptom_scores.items():
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
                moderate_risk_symptoms.append(meta["name"])

        likely = bool(red_flags or high_risk_symptoms or len(moderate_risk_symptoms) >= 3)
        summary = "This response suggests symptoms consistent with a potential concussion. Please seek clinical evaluation." if likely else "No red flags or high-risk symptom patterns were detected. Monitor closely and consult a provider if symptoms worsen."

        db.add(ConcussionAssessment(
            user_id=payload.user_id,
            timestamp=datetime.utcnow(),
            concussion_likely=likely,
            red_flags_present=bool(red_flags),
            summary=summary
        ))
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")
    finally:
        db.close()

    return {
        "concussion_likely": likely,
        "red_flags": red_flags,
        "high_risk_symptoms": high_risk_symptoms,
        "moderate_risk_symptoms": moderate_risk_symptoms,
        "summary": summary
    }