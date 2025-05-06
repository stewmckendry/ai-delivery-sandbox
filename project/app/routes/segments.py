from fastapi import APIRouter
from project.app.schemas.segment import Segment
from project.app.clients.segment_client import record_segment_data

router = APIRouter()

@router.post("/record_segment")
def record_segment(segment: Segment):
    return record_segment_data(segment.dict())