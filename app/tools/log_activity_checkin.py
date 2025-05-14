from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import ActivityCheckin, SymptomLog
from app.symptom_library import validate_symptom_ids
import json

router = APIRouter()

class ActivityCheckinRequest(BaseModel):
    user_id: str
    stage_attempted: str
    timestamp: datetime
    symptoms: Dict[str, int]
    symptoms_worsened: bool
    notes: Optional[str] = ""

@router.post("/log_activity_checkin", tags=["activity"])
def log_activity_checkin(req: ActivityCheckinRequest):
    db = SessionLocal()
    try:
        # Log activity check-in summary
        db.add(ActivityCheckin(
            user_id=req.user_id,
            stage_attempted=req.stage_attempted,
            timestamp=req.timestamp,
            symptoms_reported=json.dumps(req.symptoms),
            symptoms_worsened=req.symptoms_worsened,
            notes=req.notes
        ))

        # Log each symptom to SymptomLog
        for s_input, score in req.symptoms.items():
            try:
                validate_symptom_ids([s_input])
                canonical_id = s_input
            except Exception:
                canonical_id = "other"

            db.add(SymptomLog(
                user_id=req.user_id,
                timestamp=req.timestamp,
                symptom_id=canonical_id,
                symptom_input=s_input,
                score=int(score) if isinstance(score, int) else 1,
                notes="activity_checkin",
                log_metadata=json.dumps({"stage_attempted": req.stage_attempted})
            ))

        db.commit()
        return {"status": "ok"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()