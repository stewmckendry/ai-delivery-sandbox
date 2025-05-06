from fastapi import APIRouter
from project.app.schemas.reflection import ReflectionInput
from project.app.clients.notion_client import save_to_notion
from project.app.clients.airtable_client import save_to_airtable

router = APIRouter()

@router.post("/record_reflection")
def record_reflection(reflection: ReflectionInput):
    data = reflection.dict()
    notion_success = save_to_notion(
        session_id=data["session_id"],
        career_id=data["career_id"],
        prompt_id=data["prompt_id"],
        text=data["text"]
    )
    airtable_success = save_to_airtable(data)
    return {"notion_saved": notion_success, "airtable_saved": airtable_success}  