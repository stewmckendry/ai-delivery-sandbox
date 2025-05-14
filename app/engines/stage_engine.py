import requests
import yaml
from typing import Dict
from datetime import datetime
from collections import defaultdict
from pydantic import ValidationError
from app.models.stage import StageMap, StageResult
from app.db.database import SessionLocal
from app.db.db_models import SymptomLog

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox"
BRANCH = "sandbox-silver-tiger"
YAML_PATH = "reference/stages.yaml"

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

    def infer_stage(self, user_id: str) -> StageResult:
        db = SessionLocal()
        try:
            logs = db.query(SymptomLog).filter_by(user_id=user_id).order_by(SymptomLog.timestamp.desc()).all()
            if not logs:
                raise ValueError("No symptom logs found")

            # Group by date and get max score per day
            daily_scores = defaultdict(int)
            for log in logs:
                date_key = log.timestamp.date()
                daily_scores[date_key] = max(daily_scores[date_key], log.score or 0)

            # Count consecutive mild days ending today
            today = datetime.utcnow().date()
            consecutive_days = 0
            for offset in range(14):
                day = today - timedelta(days=offset)
                if day in daily_scores and daily_scores[day] <= 2:
                    consecutive_days += 1
                else:
                    break

            stage_num = min(consecutive_days + 1, len(self.data.stages))
            stage = next((s for s in self.data.stages if s.stage_number == stage_num), None)

            if not stage:
                raise ValueError("No matching stage")

            return StageResult(
                stage_id=stage.id,
                stage_name=stage.name,
                stage_summary=stage.guidance_phrases[0] if stage.guidance_phrases else "",
                allowed_activities=stage.allowed_activities,
                progression_criteria=stage.progression_criteria,
                matched_factors={
                    "consecutive_mild_days": consecutive_days,
                    "most_recent_mild_day": str(today if consecutive_days > 0 else "N/A"),
                    "max_score_today": daily_scores.get(today, 0)
                }
            )
        finally:
            db.close()