from fastapi import APIRouter
from project.app.schemas.reflection import ReflectionInput
from project.app.clients.notion_client import save_to_notion
from project.app.clients.airtable_client import save_to_airtable
from project.app.utils.prompt_loader import load_prompt

router = APIRouter()

@router.post("/record_reflection")
def record_reflection(reflection: ReflectionInput):
    data = reflection.dict()
    prompt = load_prompt(data["prompt_id"])

    formatted_prompt = prompt.get("intro", "") + "\n\n" + "\n".join(
        [f"{i+1}. {q}" for i, q in enumerate(prompt.get("questions", []))]
    )

    notion_success = save_to_notion(
        session_id=data["session_id"],
        career_id=data["career_id"],
        prompt_id=data["prompt_id"],
        text=data["text"],
        timestamp=data.get("timestamp"),
        prompt_content=formatted_prompt
    )
    airtable_success = save_to_airtable(data)
    return {"notion_saved": notion_success, "airtable_saved": airtable_success}