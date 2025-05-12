from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import json

from app.db.db_models import SymptomLog
from app.db.database import SessionLocal


def log_symptoms_to_db(
    user_id: str,
    injury_date: datetime,
    checkin_time: datetime,
    symptoms: dict,
    stage: str = None,
    source: str = "gpt",
    reporter_type: str = None,
    incident_context: str = None,
    sport_type: str = None,
    age_group: str = None,
    team_id: str = None
):
    """Persist symptom log to Azure SQL."""
    db: Session = SessionLocal()
    try:
        log_entry = SymptomLog(
            user_id=user_id,
            timestamp=checkin_time,
            symptoms=json.dumps(symptoms),
            log_metadata=json.dumps({"stage": stage, "source": source}),
            reporter_type=reporter_type,
            incident_context=incident_context,
            sport_type=sport_type,
            age_group=age_group,
            team_id=team_id
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()