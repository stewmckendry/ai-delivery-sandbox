from fastapi import APIRouter
from app.models.symptoms import StageInferenceRequest, StageInferenceResult
from app.models.stage import StageResult
from app.engines.stage_engine import StageEngine
from app.db.db_models import StageLog, SessionLocal
from datetime import datetime

router = APIRouter()

@router.post("/get_stage_guidance", response_model=StageInferenceResult)
def get_stage_guidance(payload: StageInferenceRequest) -> StageInferenceResult:
    # Use stage engine to infer recovery stage from symptoms
    symptoms = payload.tracker_state.answers
    injury_date = payload.tracker_state.injury_date
    days_since_injury = (payload.tracker_state.checkin_time - injury_date).days
    user_id = payload.tracker_state.user_id

    engine = StageEngine()
    result: StageResult = engine.infer_stage(symptoms, days_since_injury)

    # Save result to DB
    db = SessionLocal()
    try:
        db.add(StageLog(
            user_id=user_id,
            inferred_stage=result.id,
            timestamp=datetime.utcnow()
        ))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return StageInferenceResult(
        stage_result=result,
        message=f"You are currently in stage: {result.label}"
    )