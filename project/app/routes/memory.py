from fastapi import APIRouter, HTTPException, Query
from schemas.reflection import ReflectionInput
from schemas.summary import SummaryOutput
from utils.memory_manager import save_reflection, get_summary

router = APIRouter()

@router.post("/save_reflection")
def save_reflection_entry(reflection: ReflectionInput):
    try:
        success = save_reflection(reflection.dict())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save reflection")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/fetch_summary", response_model=SummaryOutput)
def fetch_summary(session_id: str = Query(..., description="Session ID to summarize")):
    try:
        summary = get_summary(session_id)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))