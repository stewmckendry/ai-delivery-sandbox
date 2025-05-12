from fastapi import APIRouter
from pydantic import BaseModel
from app.db.db_models import TrackerMetadata, TriageResponse, IncidentReport, SessionLocal
from datetime import datetime
import requests, yaml

router = APIRouter()

TRIAGE_MAP_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/triage_map.yaml"

class IncidentDetailRequest(BaseModel):
    user_id: str
    answers: dict  # e.g., output from triage questions

@router.post("/log_incident_detail", response_model=dict, tags=["triage"])
def log_incident_detail(data: IncidentDetailRequest):
    """
    Save the user's triage answers as metadata in the Tracker.
    Also logs each Q&A into TriageResponse and structured metadata into IncidentReport.
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

        # Load triage_map to get question text for audit
        response = requests.get(TRIAGE_MAP_URL)
        triage_yaml = yaml.safe_load(response.text)
        id_to_text = {
            q["id"]: q["prompt"]
            for stage in triage_yaml.get("triage_flow", [])
            for q in stage.get("questions", [])
        }

        # Insert each Q&A into TriageResponse
        for qid, answer in data.answers.items():
            question_text = id_to_text.get(qid, "")
            db.add(TriageResponse(
                user_id=data.user_id,
                question_id=qid,
                question_text=question_text,
                answer=str(answer),
                timestamp=datetime.utcnow()
            ))

        # Insert IncidentReport if structured fields exist
        db.merge(IncidentReport(
            user_id=data.user_id,
            injury_date=injury_date,
            reporter_role=data.answers.get("reporter_role"),
            sport_type=data.answers.get("sport_type"),
            age_group=data.answers.get("age_group"),
            team_id=data.answers.get("team_id"),
            injury_context=data.answers.get("injury_context"),
            symptoms=str(data.answers.get("symptoms")),
            lost_consciousness=data.answers.get("lost_consciousness"),
            seen_provider=data.answers.get("seen_provider"),
            diagnosed_concussion=data.answers.get("diagnosed_concussion"),
            still_symptomatic=data.answers.get("still_symptomatic"),
            cleared_to_play=data.answers.get("cleared_to_play"),
            timestamp=datetime.utcnow()
        ))

        db.commit()
        return {"status": "success", "user_id": data.user_id}
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()