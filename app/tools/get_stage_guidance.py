from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.db_models import IncidentReport, SymptomLog, StageLog, RecoveryCheck
from app.engines.stage_engine import StageEngine
import json

router = APIRouter()

class StageRequest(BaseModel):
    user_id: str
    injury_date: Optional[str] = None
    symptoms: Optional[Dict[str, int]] = None
    checkin_time: Optional[str] = None

@router.post("/get_stage_guidance", tags=["stage"])
def get_stage_guidance(req: StageRequest):
    db = SessionLocal()
    try:
        # Use overrides if provided
        injury_date = req.injury_date
        symptoms = req.symptoms
        checkin_time = req.checkin_time or datetime.utcnow().isoformat()

        # Fetch from DB if missing
        if not injury_date or not symptoms:
            incident = db.query(IncidentReport).filter_by(user_id=req.user_id).first()
            recent_symptoms = db.query(SymptomLog).filter_by(user_id=req.user_id).order_by(SymptomLog.timestamp.desc()).limit(10).all()

            if not incident or not recent_symptoms:
                raise HTTPException(status_code=400, detail="Missing injury date or symptoms. Please complete a triage check-in first.")

            if not injury_date:
                injury_date = incident.injury_date.isoformat()
            if not symptoms:
                symptoms = {}
                for s in recent_symptoms:
                    if s.symptom_id not in symptoms:
                        symptoms[s.symptom_id] = s.score or 1

        # Log to recovery_check if using overrides
        if req.symptoms or req.injury_date:
            db.add(RecoveryCheck(
                user_id=req.user_id,
                timestamp=datetime.utcnow(),
                injury_date=datetime.fromisoformat(injury_date).date(),
                symptoms=json.dumps(symptoms),
                source="quick_prompt",
                notes=""
            ))

        # Run inference
        engine = StageEngine()
        result = engine.infer_stage(
            user_id=req.user_id,
            injury_date=injury_date,
            checkin_time=checkin_time,
            symptoms=symptoms
        )

        # Log to StageLog
        db.add(StageLog(
            user_id=req.user_id,
            timestamp=datetime.utcnow(),
            result_json=json.dumps(result.dict())
        ))
        db.commit()

        return result.dict()

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()