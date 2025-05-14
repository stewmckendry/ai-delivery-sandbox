from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.database import SessionLocal
from app.db.db_models import IncidentReport, SymptomLog, ActivityCheckin
from collections import defaultdict

router = APIRouter()

class UserHistoryRequest(BaseModel):
    user_id: str

@router.post("/get_user_history", tags=["User"])
def get_user_history(req: UserHistoryRequest):
    db: Session = SessionLocal()
    try:
        # Incident report
        incident = db.query(IncidentReport).filter(IncidentReport.user_id == req.user_id).first()
        incident_logged = bool(incident)
        incident_info = {
            "injury_date": incident.injury_date.isoformat() if incident and incident.injury_date else None,
            "reporter_role": incident.reporter_role,
            "sport_type": incident.sport_type,
            "age_group": incident.age_group,
            "team_id": incident.team_id,
            "injury_context": incident.injury_context,
            "diagnosed_concussion": incident.diagnosed_concussion,
            "seen_provider": incident.seen_provider,
            "still_symptomatic": incident.still_symptomatic,
            "cleared_to_play": incident.cleared_to_play
        } if incident else None

        # Most recent symptom log timestamp
        latest_symptom_time = db.query(SymptomLog.timestamp).filter(SymptomLog.user_id == req.user_id).order_by(desc(SymptomLog.timestamp)).first()
        last_symptom_log = []
        last_symptom_log_timestamp = None
        if latest_symptom_time:
            ts = latest_symptom_time[0]
            last_symptom_log_timestamp = ts.isoformat()
            symptoms = db.query(SymptomLog).filter(SymptomLog.user_id == req.user_id, SymptomLog.timestamp == ts).all()
            last_symptom_log = [{
                "symptom_id": s.symptom_id,
                "score": s.score
            } for s in symptoms]

        # Most recent activity check-in
        last_checkin = db.query(ActivityCheckin).filter(ActivityCheckin.user_id == req.user_id).order_by(desc(ActivityCheckin.timestamp)).first()
        last_activity_checkin = {
            "stage_attempted": last_checkin.stage_attempted,
            "timestamp": last_checkin.timestamp.isoformat(),
            "symptoms_worsened": last_checkin.symptoms_worsened
        } if last_checkin else None

        # Distinct stages attempted
        stage_rows = db.query(ActivityCheckin.stage_attempted).filter(ActivityCheckin.user_id == req.user_id).distinct().all()
        stages_attempted = [s[0] for s in stage_rows]

        return {
            "incident_logged": incident_logged,
            "incident_info": incident_info,
            "last_symptom_log_timestamp": last_symptom_log_timestamp,
            "last_symptom_log": last_symptom_log,
            "last_activity_checkin": last_activity_checkin,
            "stages_attempted": stages_attempted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()