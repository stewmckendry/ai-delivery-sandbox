from pydantic import BaseModel
from typing import List, Optional

class SectionDraftOutput(BaseModel):
    prompt_used: str
    raw_draft: str
    draft_chunks: Optional[List[str]] = None
    tool_version: Optional[str] = "v1"
    schema_version: Optional[str] = "1.0"