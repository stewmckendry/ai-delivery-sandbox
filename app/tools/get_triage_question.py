from fastapi import APIRouter, Body
from pydantic import BaseModel
import requests
import yaml
from typing import Optional

router = APIRouter()

TRIAGE_MAP_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silver-tiger/reference/triage_map.yaml"

class TriageQuestionRequest(BaseModel):
    tracker_state: dict  # includes 'answers': {question_id: response, ...}
    last_question_id: Optional[str] = None

@router.post("/get_triage_question", tags=["triage"])
def get_next_triage_question(payload: TriageQuestionRequest):
    """
    Returns the next unanswered triage question from the triage flow.
    """
    response = requests.get(TRIAGE_MAP_URL)
    response.raise_for_status()
    triage_map = yaml.safe_load(response.text)

    answered_ids = set(payload.tracker_state.get("answers", {}).keys())
    found_last = payload.last_question_id is None

    for stage in triage_map.get("triage_flow", []):
        context = stage.get("name")
        for q in stage.get("questions", []):
            qid = q.get("id")
            if not found_last:
                if qid == payload.last_question_id:
                    found_last = True
                continue
            if qid not in answered_ids:
                return {
                    "id": qid,
                    "prompt": q.get("prompt"),
                    "type": q.get("type"),
                    "intent": q.get("intent"),
                    "mode": q.get("mode"),
                    "context": context,
                    "symptom_links": q.get("symptom_links", []),
                    "tool_tags": q.get("tool_tags", []),
                    "example_user_answers": q.get("example_user_answers", [])
                }

    return {"message": "Triage complete or no questions remaining."}