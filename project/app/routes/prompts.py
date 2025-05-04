from fastapi import APIRouter, Query
from utils.prompt_loader import load_prompt

router = APIRouter()

@router.get("/load_prompt")
def get_prompt(prompt_id: str = Query(..., description="ID of the coaching prompt")):
    return load_prompt(prompt_id)