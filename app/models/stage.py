from typing import List, Literal
from pydantic import BaseModel

class StageCriteriaLogic(BaseModel):
    symptom_severity_max: Literal["mild", "moderate", "severe"]  # Max allowed symptom severity label
    duration_min_hours: int  # Min hours since injury to qualify

class StageDefinition(BaseModel):
    id: str  # Unique identifier
    stage_number: int  # Sequence in recovery
    name: str  # Stage name
    description: str  # Human-readable summary
    allowed_activities: List[str]  # Suggested activities
    activity_keywords: List[str]  # NLP-friendly tags
    contraindicated_examples: List[str]  # What to avoid
    progression_criteria: List[str]  # Textual rules to move to next stage
    stage_criteria_logic: StageCriteriaLogic  # Rules used in engine
    medical_clearance_required: bool  # Whether clinician sign-off is needed
    guidance_phrases: List[str]  # Sentences to guide user
    tool_tags: List[str]  # For downstream tool logic

class StageMap(BaseModel):
    stages: List[StageDefinition]  # Complete ordered stage list

class StageResult(BaseModel):
    stage_id: str
    label: str
    guidance: str
    matched_criteria: dict