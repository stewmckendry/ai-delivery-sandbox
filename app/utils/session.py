from __future__ import annotations

from uuid import uuid4


def generate_session_key() -> str:
    """Return a new random session identifier."""
    return uuid4().hex
