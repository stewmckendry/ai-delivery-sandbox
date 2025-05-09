from pathlib import Path
from typing import List, Dict
import yaml
from pydantic import ValidationError
from app.models.triage import TriageMap, TriageQuestion

TRIAGE_YAML_PATH = Path("reference/triage_map.yaml")

class TriageEngine:
    def __init__(self, path: Path = TRIAGE_YAML_PATH):
        self.path = path
        self.data = self._load()

    def _load(self) -> TriageMap:
        with open(self.path, 'r') as f:
            raw = yaml.safe_load(f)
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