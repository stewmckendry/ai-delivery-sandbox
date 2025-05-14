from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import ActivityCheckin

router = APIRouter()

class CheckinRequest(BaseModel):
    user_id: str
    stage_attempted: str
    timestamp: datetime
    symptoms: Optional[Dict[str, int]] = Field(..., description="Dictionary of {symptom_id: score}")
    symptoms_worsened: bool
    notes: Optional[str] = None

@router.post("/log_activity_checkin", tags=["Check-in"])
def log_activity_checkin(request: CheckinRequest):
    db = SessionLocal()
    try:
        db.add(ActivityCheckin(
            user_id=request.user_id,
            timestamp=request.timestamp,
            stage_attempted=request.stage_attempted,
            symptoms_reported=request.symptoms,
            symptoms_worsened=request.symptoms_worsened,
            notes=request.notes
        ))
        db.commit()
        return {"message": "Check-in logged successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()