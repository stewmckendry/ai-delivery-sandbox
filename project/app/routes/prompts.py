from fastapi import APIRouter
from project.app.schemas.prompt import Prompt
from project.app.clients.airtable_client import get_reflections

router = APIRouter()

@router.get("/load_prompt")
def load_prompt(prompt_id: str):
    results = get_reflections(prompt_id)
    return results if results else {"error": "No records found"}