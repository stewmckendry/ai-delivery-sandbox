from typing import Dict
from datetime import datetime, date
from pydantic import BaseModel
from app.models.tracker import TrackerState
from app.models.stage import StageResult

class SymptomCheckIn(BaseModel):
    """Input schema for logging a symptom check-in"""
    user_id: str
    injury_date: date
    checkin_time: datetime
    symptoms: Dict[str, int]  # symptom_id → 0–5 severity

class SymptomLogResult(BaseModel):
    """Output schema after logging a check-in"""
    tracker_state: TrackerState
    message: str

class StageInferenceRequest(BaseModel):
    """Input to get_stage_guidance tool"""
    user_id: str
    tracker_state: TrackerState

class StageInferenceResult(BaseModel):
    """Output from get_stage_guidance tool"""
    stage_result: StageResult
    message: str