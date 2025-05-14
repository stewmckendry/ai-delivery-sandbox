from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
import json
import traceback
from app.db.database import SessionLocal
from app.db.db_models import ActivityCheckin, SymptomLog
from app.symptom_library import validate_symptom_ids

router = APIRouter()

class CheckinRequest(BaseModel):
    user_id: str
    stage_attempted: str
    timestamp: datetime
    symptoms: Dict[str, int] = Field(..., description="Dictionary of {symptom_id: score}")
    symptoms_worsened: bool
    notes: Optional[str] = None

@router.post("/log_activity_checkin", tags=["Check-in"])
def log_activity_checkin(
    req: CheckinRequest = Body(..., embed=False)
):
    print("✅ log_activity_checkin called with:", req)

    db = SessionLocal()
    try:
        db.add(ActivityCheckin(
            user_id=req.user_id,
            stage_attempted=req.stage_attempted,
            timestamp=req.timestamp,
            symptoms_reported=json.dumps(req.symptoms),
            symptoms_worsened=req.symptoms_worsened,
            notes=req.notes
        ))

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
        return {"message": "Check-in and symptoms logged successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )
    finally:
        db.close()