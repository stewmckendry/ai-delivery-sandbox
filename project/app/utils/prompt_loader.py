import json
import httpx
from fastapi import HTTPException

PROMPT_LIST_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silent-otter/project/inputs/prompts/prompts.json"

def load_prompt(prompt_id: str) -> dict:
    try:
        response = httpx.get(PROMPT_LIST_URL, timeout=5.0)
        response.raise_for_status()
        all_prompts = response.json()
        for prompt in all_prompts:
            if prompt.get("id") == prompt_id:
                return prompt
        raise HTTPException(status_code=404, detail="Prompt not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prompts: {str(e)}")