from typing import Dict
from datetime import date, datetime
from pydantic import BaseModel

class TrackerState(BaseModel):
    """
    Represents the user's current state used to infer stage and track recovery.
    """
    user_id: str  # Unique user identifier
    injury_date: date  # Date of injury
    checkin_time: datetime  # Time of this symptom check-in
    answers: Dict[str, int]  # symptom_id → 0–5 severity rating
    last_stage_id: str = None  # Optional last inferred stage
    cleared_to_play: bool = False  # Indicates if the user has been cleared