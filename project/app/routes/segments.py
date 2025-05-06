from fastapi import APIRouter
from ..schemas.segment import Segment
from ..clients.segment_client import SegmentClient

router = APIRouter()
segment_client = SegmentClient()

@router.post("/record_segment")
def record_segment(segment: Segment):
    return segment_client.record_segment(segment)