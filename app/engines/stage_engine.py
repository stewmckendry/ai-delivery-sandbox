import requests
import yaml
from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
from pydantic import ValidationError
from app.models.stage import StageMap, StageResult
from app.db.database import SessionLocal
from app.db.db_models import SymptomLog, ActivityCheckin

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
            checkin = db.query(ActivityCheckin).filter(ActivityCheckin.user_id == user_id).order_by(ActivityCheckin.timestamp.desc()).first()

            if not checkin:
                return self._assume_stage_1()

            hours_since = (datetime.utcnow() - checkin.timestamp).total_seconds() / 3600.0

            if checkin.symptoms_worsened:
                return self._regress_stage(checkin.stage_attempted)

            # Load symptom logs for same timestamp
            logs = db.query(SymptomLog).filter(SymptomLog.user_id == user_id, SymptomLog.timestamp >= checkin.timestamp).all()
            if not logs:
                raise ValueError("No recent symptom logs found after check-in")

            scores = [s.score or 0 for s in logs]
            max_score = max(scores)

            if hours_since < 24:
                return self._hold_stage(checkin.stage_attempted, max_score, hours_since)

            if max_score > 2:
                return self._regress_stage(checkin.stage_attempted)

            return self._advance_stage(checkin.stage_attempted, max_score)

        finally:
            db.close()

    def _assume_stage_1(self) -> StageResult:
        stage = next(s for s in self.data.stages if s.stage_number == 1)
        return StageResult(
            stage_id=stage.id,
            stage_name=stage.name,
            stage_summary=stage.guidance_phrases[0],
            allowed_activities=stage.allowed_activities,
            progression_criteria=stage.progression_criteria,
            matched_factors={"inference_mode": "no_activity_checkin"},
            next_step_advice="You haven’t logged any stage activity yet. Try a light activity like walking and check back in."
        )

    def _regress_stage(self, current_stage_id: str) -> StageResult:
        current_stage = next((s for s in self.data.stages if s.id == current_stage_id), None)
        fallback_num = max(current_stage.stage_number - 1, 1)
        stage = next((s for s in self.data.stages if s.stage_number == fallback_num), None)
        return StageResult(
            stage_id=stage.id,
            stage_name=stage.name,
            stage_summary=stage.guidance_phrases[0],
            allowed_activities=stage.allowed_activities,
            progression_criteria=stage.progression_criteria,
            matched_factors={"inference_mode": "regressed_due_to_symptom_worsening"},
            next_step_advice="Symptoms worsened during the last stage. Let’s return to a lower stage and ease back in."
        )

    def _hold_stage(self, stage_id: str, score: int, hours: float) -> StageResult:
        stage = next((s for s in self.data.stages if s.id == stage_id), None)
        return StageResult(
            stage_id=stage.id,
            stage_name=stage.name,
            stage_summary=stage.guidance_phrases[0],
            allowed_activities=stage.allowed_activities,
            progression_criteria=stage.progression_criteria,
            matched_factors={
                "inference_mode": "waiting_period",
                "max_score": score,
                "hours_since_checkin": hours
            },
            next_step_advice="You’re doing well. Let’s give it a full 24 hours symptom-free before progressing."
        )

    def _advance_stage(self, current_stage_id: str, score: int) -> StageResult:
        current = next((s for s in self.data.stages if s.id == current_stage_id), None)
        next_stage = next((s for s in self.data.stages if s.stage_number == current.stage_number + 1), None)
        return StageResult(
            stage_id=next_stage.id,
            stage_name=next_stage.name,
            stage_summary=next_stage.guidance_phrases[0],
            allowed_activities=next_stage.allowed_activities,
            progression_criteria=next_stage.progression_criteria,
            matched_factors={
                "inference_mode": "confirmed",
                "max_score": score,
                "consecutive_mild_days": 1
            },
            next_step_advice="Great progress! You’re ready to move to the next stage."
        )