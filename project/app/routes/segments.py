from fastapi import APIRouter
from project.app.schemas.segment import Segment

router = APIRouter()

@router.post("/record_segment")
def record_segment(segment: Segment):
    return {"message": "Segment recorded (stub)"}