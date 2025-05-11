from fastapi import APIRouter
import requests
import yaml

router = APIRouter()

TRIAGE_MAP_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/triage_map.yaml"

@router.get("/get_triage_flow", tags=["triage"])
def get_triage_flow():
    """
    Load and return a GPT-friendly triage flow map.
    Flattens stage/questions into a list with stage context.
    Clarifies intent for each mode and includes linked symptom IDs.
    """
    response = requests.get(TRIAGE_MAP_URL)
    response.raise_for_status()
    triage_yaml = yaml.safe_load(response.text)

    flat_questions = []
    for stage in triage_yaml.get("triage_flow", []):
        context = stage.get("name")
        for q in stage.get("questions", []):
            mode_description = "ask for details" if q.get("mode") == "probe" else "ask for confirmation"
            flat_questions.append({
                "id": q.get("id"),
                "prompt": q.get("prompt"),
                "type": q.get("type"),
                "intent": q.get("intent"),
                "mode": q.get("mode"),
                "mode_description": mode_description,
                "example_user_answers": q.get("example_user_answers"),
                "context": context,
                "tool_tags": q.get("tool_tags", []),
                "symptom_links": q.get("symptom_links", [])
            })

    return {"questions": flat_questions}