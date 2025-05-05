from pydantic import BaseModel
from typing import List, Optional

class CareerCard(BaseModel):
    title: str
    metaphor: Optional[str]
    category: Optional[str]
    skills: Optional[List[str]]
    traits: Optional[List[str]]
    path: Optional[str]

class Segment(BaseModel):
    careers: List[CareerCard]