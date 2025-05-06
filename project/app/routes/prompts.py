from fastapi import APIRouter
from project.app.utils import prompt_loader

router = APIRouter()

@router.get("/load_prompt")
def load_prompt(prompt_id: str):
    prompt = prompt_loader.load_prompt(prompt_id)
    if not prompt:
        return {"error": "Prompt not found"}
    return prompt