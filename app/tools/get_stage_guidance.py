from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from app.db.database import SessionLocal
from app.db.db_models import IncidentReport, RecoveryCheck, StageLog
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
        # Log override if present
        if req.symptoms or req.injury_date:
            db.add(RecoveryCheck(
                user_id=req.user_id,
                timestamp=datetime.utcnow(),
                injury_date=datetime.fromisoformat(req.injury_date).date() if req.injury_date else None,
                symptoms=json.dumps(req.symptoms or {}),
                source="quick_prompt",
                notes=""
            ))

        # Infer stage
        engine = StageEngine()
        result = engine.infer_stage(user_id=req.user_id)

        # Log structured result
        db.add(StageLog(
            user_id=req.user_id,
            stage_id=result.stage_id,
            stage_name=result.stage_name,
            mild_days=result.matched_factors.get("consecutive_mild_days", 0),
            max_score_today=result.matched_factors.get("max_score_today", 0),
            recent_mild_day=result.matched_factors.get("most_recent_mild_day", None),
            timestamp=datetime.utcnow()
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