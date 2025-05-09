from fastapi import APIRouter
from app.models.symptoms import StageInferenceRequest, StageInferenceResult
from app.models.stage import StageResult
from app.engines.stage_engine import StageEngine

router = APIRouter()

@router.post("/get_stage_guidance", response_model=StageInferenceResult)
def get_stage_guidance(payload: StageInferenceRequest) -> StageInferenceResult:
    # Use stage engine to infer recovery stage from symptoms
    symptoms = payload.tracker_state.answers
    injury_date = payload.tracker_state.injury_date
    days_since_injury = (payload.tracker_state.checkin_time - injury_date).days

    engine = StageEngine()
    result: StageResult = engine.infer_stage(symptoms, days_since_injury)

    return StageInferenceResult(
        stage_result=result,
        message=f"You are currently in stage: {result.label}"
    )