from fastapi import APIRouter
from ..schemas.reflection import ReflectionInput
from ..clients.notion_client import NotionClient

router = APIRouter()
notion_client = NotionClient()

@router.post("/record_reflection")
def record_reflection(reflection: ReflectionInput):
    return notion_client.record_reflection(reflection)