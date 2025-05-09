import requests
import yaml
from typing import List, Dict
from pydantic import ValidationError
from app.models.triage import TriageMap

# Constants for remote YAML access
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox"
BRANCH = "sandbox-silver-tiger"
YAML_PATH = "reference/triage_map.yaml"

class TriageEngine:
    def __init__(self, url: str = None):
        self.url = url or f"{GITHUB_RAW_BASE}/{BRANCH}/{YAML_PATH}"
        self.data = self._load()

    def _load(self) -> TriageMap:
        response = requests.get(self.url)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to load triage YAML: {response.status_code}")
        raw = yaml.safe_load(response.text)
        try:
            return TriageMap(**raw)
        except ValidationError as e:
            raise ValueError(f"Invalid triage map: {e}")

    def get_next_question(self, tracker_state: Dict[str, str]) -> Dict:
        answered = tracker_state.get("answers", {})
        for stage in self.data.triage_flow:
            for q in stage.questions:
                if q.id not in answered:
                    return {
                        "question": q.prompt,
                        "options": q.options if q.options else [],
                        "is_terminal": False
                    }
        return {"is_terminal": True}

    def evaluate_flags(self, tracker_state: Dict[str, str]) -> List[str]:
        flags = []
        answers = tracker_state.get("answers", {})
        for stage in self.data.triage_flow:
            for q in stage.questions:
                if q.red_flag_check and q.id in answers:
                    flags.append(q.id)
        return flags