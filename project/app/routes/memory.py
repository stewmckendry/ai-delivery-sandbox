from fastapi import APIRouter, HTTPException
from schemas.reflection import ReflectionInput
from utils.memory_manager import save_reflection

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