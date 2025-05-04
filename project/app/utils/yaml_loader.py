import yaml
import httpx
from fastapi import HTTPException

SEGMENT_URL_TEMPLATE = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-silent-otter/project/inputs/knowledgebooks/segments/youth_career_guide_{category}.yaml"

def load_segment(category: str) -> dict:
    url = SEGMENT_URL_TEMPLATE.format(category=category)
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Career segment not found")
        response.raise_for_status()
        return yaml.safe_load(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading segment: {str(e)}")