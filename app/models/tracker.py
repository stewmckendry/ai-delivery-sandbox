from typing import Dict
from pydantic import BaseModel

class TrackerState(BaseModel):
    """
    Represents the user's progress through triage or recovery check-ins.
    Used as input to triage and stage engines.

    The keys in the `answers` dict must match the `id` of each question defined in triage_map.yaml.
    For example, if a question has id: "injury_date" in triage_flow, it should appear here as:
      answers = {"injury_date": "2024-01-01"}
    """
    answers: Dict[str, str]  # Maps question ID to the user's answer (e.g., {"q1": "Hit"})