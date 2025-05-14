from fastapi import APIRouter
import requests
import yaml

router = APIRouter()

CHECKIN_MAP_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/checkin_map.yaml"

@router.get("/get_checkin_flow", tags=["checkin"])
def get_checkin_flow():
    """
    Load and return a GPT-friendly activity/symptom check-in map.
    Flattens stages/questions into a list with essential fields only.
    """
    response = requests.get(CHECKIN_MAP_URL)
    response.raise_for_status()
    checkin_yaml = yaml.safe_load(response.text)

    flat_questions = []
    for stage in checkin_yaml.get("checkin_flow", []):
        for q in stage.get("questions", []):
            flat_questions.append({
                "id": q.get("id"),
                "prompt": q.get("prompt"),
                "type": q.get("type"),
                "intent": q.get("intent"),
                "mode": q.get("mode"),
                "example_user_answers": q.get("example_user_answers"),
                "response_parsing": q.get("response_parsing")
            })

    return {"questions": flat_questions}