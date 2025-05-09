import requests
import yaml
from typing import Dict, Any
from pydantic import ValidationError
from app.models.stage import StageMap, StageResult
from app.models.tracker import TrackerState

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox"
BRANCH = "sandbox-silver-tiger"
YAML_PATH = "reference/stages.yaml"

SEVERITY_CUTOFFS = {
    "mild": 5,
    "moderate": 10,
    "severe": 15
}

class StageEngine:
    def __init__(self, url: str = None):
        self.url = url or f"{GITHUB_RAW_BASE}/{BRANCH}/{YAML_PATH}"
        self.data = self._load()

    def _load(self) -> StageMap:
        response = requests.get(self.url)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to load stage YAML: {response.status_code}")
        raw = yaml.safe_load(response.text)
        try:
            return StageMap(**raw)
        except ValidationError as e:
            raise ValueError(f"Invalid stage map: {e}")

    def infer_stage(self, symptoms: Dict[str, int], days_since_injury: int) -> StageResult:
        hours_since_injury = days_since_injury * 24
        severity_score = sum(symptoms.values())

        for stage in self.data.stages:
            logic = stage.stage_criteria_logic
            if (
                hours_since_injury >= logic.duration_min_hours and
                severity_score <= SEVERITY_CUTOFFS.get(logic.symptom_severity_max, 99)
            ):
                return StageResult(
                    stage_id=stage.id,
                    label=stage.name,
                    guidance=stage.guidance_phrases[0] if stage.guidance_phrases else "",
                    matched_criteria={
                        "hours": hours_since_injury,
                        "symptom_score": severity_score
                    }
                )

        raise ValueError("No matching stage found for given inputs")