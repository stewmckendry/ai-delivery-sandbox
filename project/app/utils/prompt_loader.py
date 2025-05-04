import json
import httpx
from fastapi import HTTPException

RAW_BASE_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silent-otter/project/inputs/prompts"

def load_prompt(prompt_id: str) -> dict:
    url = f"{RAW_BASE_URL}/{prompt_id}.json"
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Prompt not found")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prompt: {str(e)}")