from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Union
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import ActivityCheckin, SymptomLog
from app.symptom_library import validate_symptom_ids
import json

router = APIRouter()

class CheckinLogRequest(BaseModel):
    user_id: str
    timestamp: datetime
    answers: Dict[str, Union[str, Dict[str, Union[str, int, float]], bool]]

@router.post("/log_checkin_gptfix", tags=["Check-in"])
def log_checkin_gptfix(request: CheckinLogRequest):
    db = SessionLocal()
    try:
        structured = {}
        for field in ["stage_attempted", "symptoms", "symptoms_worsened", "notes"]:
            if field in request.answers:
                structured[field] = request.answers[field]

        if "symptoms" in structured and isinstance(structured["symptoms"], dict):
            structured["symptoms_reported"] = json.dumps(structured.pop("symptoms"))

        if structured:
            db.add(ActivityCheckin(
                user_id=request.user_id,
                timestamp=request.timestamp,
                **structured
            ))

        symptom_dict = request.answers.get("symptoms", {})
        if isinstance(symptom_dict, dict):
            for s_input, score in symptom_dict.items():
                try:
                    validate_symptom_ids([s_input])
                    canonical_id = s_input
                except Exception:
                    canonical_id = "other"
                db.add(SymptomLog(
                    user_id=request.user_id,
                    timestamp=request.timestamp,
                    symptom_id=canonical_id,
                    symptom_input=s_input,
                    score=int(score) if isinstance(score, int) else 1,
                    notes="activity_checkin",
                    log_metadata=json.dumps({"stage_attempted": request.answers.get("stage_attempted", "")})
                ))

        db.commit()
        return {"status": "ok"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()