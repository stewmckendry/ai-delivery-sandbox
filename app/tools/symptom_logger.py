import json
from typing import Dict
from fastapi import APIRouter
from app.models.symptoms import SymptomCheckIn, SymptomLogResult
from app.models.tracker import TrackerState
from app.db.db_writer import log_symptoms_to_db
from app.db.db_models import TrackerMetadata, SessionLocal
from app.symptom_library import validate_symptom_ids

router = APIRouter()

@router.post("/log_symptoms", response_model=SymptomLogResult)
def log_symptoms(payload: SymptomCheckIn) -> SymptomLogResult:
    # Validate symptom IDs using shared library
    validate_symptom_ids(list(payload.symptoms.keys()))

    state = TrackerState(answers=payload.symptoms)
    metadata = payload.metadata or {}

    db = SessionLocal()
    try:
        existing = db.query(TrackerMetadata).filter_by(user_id=payload.user_id).first()
    finally:
        db.close()

    def get_meta(field):
        return metadata.get(field) or payload.symptoms.get(field) or getattr(existing, field, None)

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