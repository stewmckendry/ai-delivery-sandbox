from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import SymptomLog
import json

router = APIRouter()

class SymptomLogRequest(BaseModel):
    user_id: str
    timestamp: datetime
    symptoms: List[str]

@router.post("/log_symptoms", tags=["symptoms"])
def log_symptoms(request: SymptomLogRequest):
    db = SessionLocal()
    try:
        db.add(SymptomLog(
            user_id=request.user_id,
            timestamp=request.timestamp,
            symptoms=json.dumps(request.symptoms),
            log_metadata="{}",
            incident_context="",
            reporter_type="",
            sport_type="",
            age_group="",
            team_id="",
            extra_notes=""
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to log symptoms: {str(e)}")
    finally:
        db.close()

    return {"status": "ok", "message": "Symptoms logged successfully."}