from fastapi import APIRouter
import requests
import yaml

router = APIRouter()

TRIAGE_MAP_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/triage_map.yaml"

@router.get("/get_triage_flow", tags=["triage"])
def get_triage_flow():
    """
    Load and return a GPT-friendly triage flow map.
    Flattens stage/questions into a list with essential fields only.
    """
    response = requests.get(TRIAGE_MAP_URL)
    response.raise_for_status()
    triage_yaml = yaml.safe_load(response.text)

    flat_questions = []
    for stage in triage_yaml.get("triage_flow", []):
        for q in stage.get("questions", []):
            flat_questions.append({
                "id": q.get("id"),
                "prompt": q.get("prompt"),
                "type": q.get("type"),
                "intent": q.get("intent"),
                "mode": q.get("mode"),
                "example_user_answers": q.get("example_user_answers"),
                "symptom_links": q.get("symptom_links", []),
                "skip_if": q.get("skip_if", {})
            })

    return {"questions": flat_questions}