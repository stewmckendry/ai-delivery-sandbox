import json
import requests
import yaml
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import SymptomLog

router = APIRouter()

SYMPTOM_YAML_URLS = [
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_red_flag.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_physical.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_emotional.yaml",
    "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/symptoms_sleep.yaml",
]

class SymptomEntry(BaseModel):
    symptom_input: str
    score: int
    notes: str = ""

class SymptomCheckPayload(BaseModel):
    user_id: str
    timestamp: datetime
    symptoms: List[SymptomEntry]

@router.post("/log_symptoms")
def log_symptoms(payload: SymptomCheckPayload):
    # Load reference symptom list
    known_symptoms = {}
    for url in SYMPTOM_YAML_URLS:
        response = requests.get(url)
        response.raise_for_status()
        yaml_data = yaml.safe_load(response.text)
        for s in yaml_data.get("symptoms", []):
            known_symptoms[s["name"].lower()] = s["id"]

    db = SessionLocal()
    try:
        for entry in payload.symptoms:
            canonical_id = known_symptoms.get(entry.symptom_input.lower(), "other")
            log = SymptomLog(
                user_id=payload.user_id,
                timestamp=payload.timestamp,
                symptom_id=canonical_id,
                symptom_input=entry.symptom_input,
                score=entry.score,
                notes=entry.notes,
                log_metadata="{}"
            )
            db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error logging symptoms: {str(e)}")
    finally:
        db.close()

    return {"status": "ok", "message": "Symptoms logged successfully."}