from typing import List, Literal, Dict, Any
from pydantic import BaseModel

class StageCriteriaLogic(BaseModel):
    symptom_severity_max: Literal["mild", "moderate", "severe"]
    duration_min_hours: int

class StageDefinition(BaseModel):
    id: str
    stage_number: int
    name: str
    description: str
    allowed_activities: List[str]
    activity_keywords: List[str]
    contraindicated_examples: List[str]
    progression_criteria: List[str]
    stage_criteria_logic: StageCriteriaLogic
    medical_clearance_required: bool
    guidance_phrases: List[str]
    tool_tags: List[str]

class StageMap(BaseModel):
    stages: List[StageDefinition]

class StageResult(BaseModel):
    stage_id: str
    stage_name: str
    stage_summary: str
    allowed_activities: List[str]
    progression_criteria: List[str]
    matched_factors: Dict[str, Any]