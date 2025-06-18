from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.storage import audit
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])


class ConsentPayload(BaseModel):
    user_id: str
    portal_name: str
    action: str
    timestamp: datetime


@router.post("/consent")
def record_consent(payload: ConsentPayload) -> dict[str, str]:
    """Record user consent for portal automation."""
    audit.log_event(
        payload.user_id,
        payload.action,
        {"portal": payload.portal_name, "timestamp": payload.timestamp.isoformat()},
    )
    return {"status": "consent recorded"}
