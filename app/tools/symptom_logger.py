import json
import yaml
import requests
from typing import Dict
from fastapi import APIRouter
from app.models.symptoms import SymptomCheckIn, SymptomLogResult
from app.models.tracker import TrackerState
from app.db.db_writer import log_symptoms_to_db  # DB write logic
from app.db.db_models import TrackerMetadata, SessionLocal

router = APIRouter()

# GitHub raw paths
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox"
BRANCH = "sandbox-silver-tiger"
SYMPTOM_YAML_PATHS = [
    "reference/symptoms_physical.yaml",
    "reference/symptoms_emotional.yaml",
    "reference/symptoms_sleep.yaml",
    "reference/symptoms_red_flag.yaml",
]

KNOWN_SYMPTOMS = {}
for path in SYMPTOM_YAML_PATHS:
    url = f"{GITHUB_RAW_BASE}/{BRANCH}/{path}"
    response = requests.get(url)
    if response.status_code == 200:
        data = yaml.safe_load(response.text)
        for entry in data.get("symptoms", []):
            KNOWN_SYMPTOMS[entry["id"]] = entry

@router.post("/log_symptoms", response_model=SymptomLogResult)
def log_symptoms(payload: SymptomCheckIn) -> SymptomLogResult:
    # Validate symptom IDs
    for sid in payload.symptoms.keys():
        if sid not in KNOWN_SYMPTOMS:
            raise ValueError(f"Unknown symptom ID: {sid}")

    # Construct tracker state
    state = TrackerState(answers=payload.symptoms)

    # Resolve metadata: prefer payload.metadata, fallback to TrackerState.answers, fallback to DB
    metadata = payload.metadata or {}

    db = SessionLocal()
    try:
        existing = db.query(TrackerMetadata).filter_by(user_id=payload.user_id).first()
    finally:
        db.close()

    def get_meta(field):
        return metadata.get(field) or payload.symptoms.get(field) or getattr(existing, field, None)

    # Write to database
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