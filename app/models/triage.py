from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class TriageQuestion(BaseModel):
    id: str  # Unique ID for the question
    prompt: str  # Text to display to the user
    type: str  # Question type (e.g., multiple-choice, yes/no)
    intent: Optional[str]  # Purpose of the question (e.g., detect mechanism)
    mode: Optional[str]  # Display or response mode (e.g., single, multi)
    response_parsing: Optional[str]  # Logic for parsing user input
    symptom_links: Optional[List[str]]  # IDs of symptoms this question maps to
    red_flag_check: Optional[bool] = False  # Flag if response is a potential danger
    tool_tags: Optional[List[str]]  # Used by tools to tag behavior
    example_user_answers: Optional[List[str]]  # Example phrases from users
    followup_conditions: Optional[List[Dict[str, Any]]]  # Conditional logic for next questions

class TriageStage(BaseModel):
    id: str  # Unique ID for the stage
    name: str  # Human-readable name
    description: Optional[str]  # Optional text describing this stage
    questions: List[TriageQuestion]  # Questions to ask in this stage

class TriageMap(BaseModel):
    triage_flow: List[TriageStage]  # Ordered list of stages in the flow