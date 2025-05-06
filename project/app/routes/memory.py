from fastapi import APIRouter
from project.app.schemas.reflection import ReflectionInput
from project.app.clients.notion_client import save_to_notion

router = APIRouter()

@router.post("/record_reflection")
def record_reflection(reflection: ReflectionInput):
    data = reflection.dict()
    success = save_to_notion(
        session_id=data["session_id"],
        career_id=data["career_id"],
        prompt_id=data["prompt_id"],
        text=data["text"]
    )
    return {"success": success}