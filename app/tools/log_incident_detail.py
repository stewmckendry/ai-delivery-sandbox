from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Union
from datetime import datetime
from app.db.db_models import TriageResponse, IncidentReport, SymptomLog
from app.db.database import SessionLocal
from app.symptom_library import validate_symptom_ids
import json

router = APIRouter()

class IncidentLogRequest(BaseModel):
    user_id: str
    timestamp: datetime
    answers: Dict[str, Union[str, List[str], bool]]

@router.post("/log_incident_detail")
def log_incident_detail(request: IncidentLogRequest):
    db = SessionLocal()
    try:
        # Save triage responses
        for qid, answer in request.answers.items():
            if qid == "symptoms":
                continue
            db.add(TriageResponse(
                user_id=request.user_id,
                question_id=qid,
                question_text=qid,
                answer=str(answer),
                timestamp=request.timestamp
            ))

        # Prepare incident report fields
        structured = {}
        for field in [
            "injury_date", "reporter_role", "sport_type", "age_group",
            "team_id", "injury_context", "symptoms", "lost_consciousness",
            "seen_provider", "diagnosed_concussion", "still_symptomatic",
            "cleared_to_play"
        ]:
            if field in request.answers:
                structured[field] = request.answers[field]

        # Handle datetime parsing
        if "injury_date" in structured and isinstance(structured["injury_date"], str):
            try:
                structured["injury_date"] = datetime.fromisoformat(structured["injury_date"])
            except Exception:
                structured["injury_date"] = datetime.utcnow()

        # Save incident report
        if structured:
            db.add(IncidentReport(
                user_id=request.user_id,
                timestamp=request.timestamp,
                **structured
            ))

        # Save individual symptom logs
        symptom_list = structured.get("symptoms", [])
        if isinstance(symptom_list, list):
            for s in symptom_list:
                try:
                    validate_symptom_ids([s])
                    canonical_id = s
                except Exception:
                    canonical_id = "other"
                db.add(SymptomLog(
                    user_id=request.user_id,
                    timestamp=request.timestamp,
                    symptom_id=canonical_id,
                    symptom_input=s,
                    score=1,
                    notes="",
                    log_metadata="{}"
                ))

        db.commit()
    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}
    finally:
        db.close()

    return {"status": "ok"}