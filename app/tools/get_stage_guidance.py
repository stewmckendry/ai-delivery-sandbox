from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from app.engines.stage_engine import StageEngine
from app.models.stage import StageResult
from app.db.database import SessionLocal
from app.db.db_models import StageLog

router = APIRouter()

class StageGuidanceRequest(BaseModel):
    user_id: str
    injury_date: Optional[str] = None
    symptoms: Optional[Dict[str, int]] = None
    checkin_time: Optional[datetime] = None

@router.post("/get_stage_guidance")
def get_stage_guidance(req: StageGuidanceRequest):
    engine = StageEngine()
    result: StageResult = engine.infer_stage(
        user_id=req.user_id,
        injury_date=req.injury_date,
        symptoms=req.symptoms,
        checkin_time=req.checkin_time
    )

    db = SessionLocal()
    try:
        db.add(StageLog(
            user_id=req.user_id,
            timestamp=datetime.utcnow(),
            stage_id=result.stage_id,
            stage_name=result.stage_name,
            mild_days=result.mild_days or 0,
            max_score_today=result.max_score_today or 0,
            recent_mild_day=result.recent_mild_day,
            inference_mode=result.inference_mode,
            matched_factors=result.matched_factors or {}
        ))
        db.commit()
    finally:
        db.close()

    return {
        "stage": result.stage_id,
        "stage_name": result.stage_name,
        "stage_summary": result.stage_summary,
        "next_step_advice": result.next_step_advice,
        "allowed_activities": result.allowed_activities,
        "progression_criteria": result.progression_criteria
    }