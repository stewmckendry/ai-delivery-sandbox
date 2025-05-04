from fastapi import APIRouter, Query
from utils.yaml_loader import load_segment

router = APIRouter()

@router.get("/get_yaml_segment")
def get_segment(category: str = Query(..., description="Career segment category (e.g. stem, creative)")):
    return load_segment(category)