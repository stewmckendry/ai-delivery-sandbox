from fastapi import APIRouter, HTTPException
from project.app.utils.yaml_loader import load_segment

router = APIRouter()

@router.get("/get_yaml_segment")
def get_yaml_segment(category: str):
    try:
        return load_segment(category)
    except HTTPException as e:
        return {"error": e.detail}