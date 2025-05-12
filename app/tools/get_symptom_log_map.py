from fastapi import APIRouter
import yaml

router = APIRouter()

@router.get("/get_symptom_log_map")
def get_symptom_log_map():
    """Return structured schema for symptom follow-up logging."""
    path = "reference/symptom_log_map.yaml"
    with open(path, "r") as f:
        parsed = yaml.safe_load(f)
    return parsed