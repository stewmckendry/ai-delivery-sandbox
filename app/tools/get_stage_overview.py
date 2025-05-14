from fastapi import APIRouter
from app.engines.stage_engine import StageEngine

router = APIRouter()

@router.get("/get_stage_overview", tags=["stage"])
def get_stage_overview():
    engine = StageEngine()
    stage_map = engine.data.stages
    return [
        {
            "stage_id": s.id,
            "stage_number": s.stage_number,
            "name": s.name,
            "summary": s.guidance_phrases[0] if s.guidance_phrases else "",
            "activities": s.allowed_activities
        }
        for s in stage_map
    ]