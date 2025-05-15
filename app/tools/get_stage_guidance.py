from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.engines.stage_engine import StageEngine
from app.db.database import SessionLocal
from app.db.db_models import StageLog

router = APIRouter()

class StageGuidanceRequest(BaseModel):
    user_id: str

@router.post("/get_stage_guidance", tags=["Assessment"])
def get_stage_guidance(req: StageGuidanceRequest):
    db: Session = SessionLocal()
    try:
        result = StageEngine().infer_stage(req.user_id)

        db.add(StageLog(
            user_id=req.user_id,
            timestamp=datetime.utcnow(),
            stage_id=result.stage_id,
            stage_name=result.stage_name,
            mild_days=result.matched_factors.get("mild_days"),
            max_score_today=result.matched_factors.get("max_score_today"),
            recent_mild_day=result.matched_factors.get("recent_mild_day"),
            inference_mode=result.matched_factors.get("inference_mode"),
            matched_factors=result.matched_factors
        ))
        db.commit()

        return {
            "stage": result.stage_id,
            "stage_name": result.stage_name,
            "stage_summary": result.stage_summary,
            "next_step_advice": result.next_step_advice,
            "allowed_activities": result.allowed_activities,
            "progression_criteria": result.progression_criteria
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()