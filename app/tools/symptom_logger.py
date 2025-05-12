import json
from typing import Dict
from fastapi import APIRouter
from app.models.symptoms import SymptomCheckIn, SymptomLogResult
from app.models.tracker import TrackerState
from app.db.db_writer import log_symptoms_to_db
from app.symptom_library import validate_symptom_ids
from app.db.db_models import SessionLocal, IncidentReport

router = APIRouter()

@router.post("/log_symptoms", response_model=SymptomLogResult)
def log_symptoms(payload: SymptomCheckIn) -> SymptomLogResult:
    validate_symptom_ids(list(payload.symptoms.keys()))

    state = TrackerState(answers=payload.symptoms)
    metadata = payload.metadata or {}

    db = SessionLocal()
    try:
        incident = db.query(IncidentReport).filter_by(user_id=payload.user_id).order_by(IncidentReport.timestamp.desc()).first()
    finally:
        db.close()

    def get_meta(field):
        return (
            metadata.get(field)
            or payload.symptoms.get(field)
            or (getattr(incident, field, None) if incident else None)
        )

    log_symptoms_to_db(
        user_id=payload.user_id,
        injury_date=payload.injury_date,
        checkin_time=payload.checkin_time,
        symptoms=payload.symptoms,
        stage=None,
        source="gpt",
        reporter_type=get_meta("reporter_type"),
        incident_context=get_meta("incident_context"),
        sport_type=get_meta("sport_type"),
        age_group=get_meta("age_group"),
        team_id=get_meta("team_id")
    )