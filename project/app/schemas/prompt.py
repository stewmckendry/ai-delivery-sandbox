from pydantic import BaseModel
from typing import List

class Prompt(BaseModel):
    intro: str
    questions: List[str]