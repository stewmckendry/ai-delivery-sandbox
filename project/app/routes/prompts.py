from fastapi import APIRouter
from ..schemas.prompt import Prompt
from ..clients.airtable_client import AirtableClient

router = APIRouter()
airtable_client = AirtableClient()

@router.get("/load_prompt")
def load_prompt(prompt_id: str):
    return airtable_client.load_prompt(prompt_id)