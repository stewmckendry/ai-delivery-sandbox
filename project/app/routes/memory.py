from fastapi import APIRouter
from project.app.schemas.reflection import ReflectionInput
from project.app.clients.notion_client import save_to_notion

router = APIRouter()

@router.post("/record_reflection")
def record_reflection(reflection: ReflectionInput):
    success = save_to_notion(reflection.dict())
    return {"success": success}