from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
import requests
import yaml
from datetime import datetime
from app.db.db_models import ConcussionAssessment
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
        db.add(ConcussionAssessment(
            user_id=payload.user_id,
            timestamp=datetime.utcnow(),
            concussion_likely=False,
            red_flags_present=False,
            summary="Assessment logic pending implementation."
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error storing assessment: {str(e)}")
    finally:
        db.close()

    return {
        "concussion_likely": False,
        "summary": "Assessment tool is now active but requires DB context. Send only user_id."
    }