from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from app.db.db_models import TriageResponse, IncidentReport
from app.db.database import SessionLocal
from app.symptom_library import validate_symptom_ids

router = APIRouter()

class IncidentLogRequest(BaseModel):
    user_id: str
    timestamp: datetime
    answers: Dict[str, str]

@router.post("/log_incident_detail")
def log_incident_detail(request: IncidentLogRequest):
    db = SessionLocal()
    try:
        for qid, answer in request.answers.items():
            if qid == "symptoms":
                continue
            db.add(TriageResponse(
                user_id=request.user_id,
                question_id=qid,
                question_text=qid,
                answer=answer,
                timestamp=request.timestamp
            ))

        structured = {}
        for field in [
            "injury_date", "reporter_role", "sport_type", "age_group",
            "team_id", "injury_context", "symptoms", "lost_consciousness",
            "seen_provider", "diagnosed_concussion", "still_symptomatic",
            "cleared_to_play"
        ]:
            if field in request.answers:
                structured[field] = request.answers[field]

        if "symptoms" in structured:
            try:
                sym_ids = eval(structured["symptoms"]).keys()
                validate_symptom_ids(list(sym_ids))
            except Exception:
                pass

        if structured:
            db.add(IncidentReport(
                user_id=request.user_id,
                timestamp=request.timestamp,
                **structured
            ))

        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return {"status": "ok"}