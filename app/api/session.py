from __future__ import annotations

from fastapi import APIRouter, Depends

from app.utils import generate_session_key
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])


@router.get("/session")
def new_session() -> dict[str, str]:
    """Return a freshly generated session key."""
    return {"session_key": generate_session_key()}
