from fastapi import APIRouter
from pydantic import BaseModel
from app.db.db_models import TrackerMetadata, SessionLocal
from datetime import datetime

router = APIRouter()

class IncidentDetailRequest(BaseModel):
    user_id: str
    answers: dict  # e.g., output from triage questions

@router.post("/log_incident_detail", response_model=dict, tags=["triage"])
def log_incident_detail(data: IncidentDetailRequest):
    """
    Save the user's triage answers as metadata in the Tracker.
    Called after GPT completes triage dialog.
    """
    db = SessionLocal()
    try:
        injury_date = data.answers.get("injury_date")
        if isinstance(injury_date, str):
            injury_date = datetime.fromisoformat(injury_date)

        metadata = TrackerMetadata(
            user_id=data.user_id,
            injury_date=injury_date,
            last_checkin_time=datetime.utcnow(),
            last_stage_id="triage_started",
            cleared_to_play=False,
            answers=data.answers
        )
        db.merge(metadata)
        db.commit()
        return {"status": "success", "user_id": data.user_id}
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()