from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
import json

from app.db.db_models import SymptomLog, TrackerMetadata, SessionLocal


def log_symptoms_to_db(user_id: str, injury_date: datetime, checkin_time: datetime, symptoms: dict, stage: str = None, source: str = "gpt"):
    """Persist symptom log and update tracker state in Azure SQL."""
    db: Session = SessionLocal()
    try:
        # Create a new symptom log record
        log_entry = SymptomLog(
            id=str(uuid4()),  # Unique log ID
            user_id=user_id,
            checkin_time=checkin_time,
            injury_date=injury_date,
            symptoms=json.dumps(symptoms),  # Store symptoms as JSON string
            stage_inferred=stage,
            source=source
        )
        db.add(log_entry)

        # Fetch or create the user's tracker metadata
        metadata = db.query(TrackerMetadata).filter_by(user_id=user_id).first()
        if not metadata:
            metadata = TrackerMetadata(
                user_id=user_id,
                injury_date=injury_date,
                last_stage_id=stage or "",
                cleared_to_play=False,
                last_checkin_time=checkin_time
            )
        else:
            # Update last check-in and optionally stage
            metadata.last_checkin_time = checkin_time
            if stage:
                metadata.last_stage_id = stage

        db.merge(metadata)  # Insert or update tracker state
        db.commit()  # Save all changes
    except Exception as e:
        db.rollback()  # Rollback if there's an error
        raise  # Re-raise for caller to handle
    finally:
        db.close()  # Always close session