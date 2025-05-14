from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Dict, Optional, Union
from datetime import datetime

router = APIRouter()

class CheckinRequest(BaseModel):
    user_id: str
    stage_attempted: str
    timestamp: datetime
    symptoms: Dict[str, Union[int, str, float]] = Field(..., description="Dictionary of {symptom_id: score}")
    symptoms_worsened: bool
    notes: Optional[str] = None

@router.post("/log_checkin_gptfix", tags=["Check-in"])
def log_checkin_gptfix(
    req: CheckinRequest = Body(..., embed=False)
):
    print("✅ log_checkin_gptfix received:", req)
    return {"message": "Check-in payload received successfully", "data": req}  # For debug visibility