"""Utility functions for short-lived delegation tokens."""
from __future__ import annotations

from datetime import datetime, timedelta
import base64
import hashlib
import hmac
import json
import os
from typing import Dict, Optional

SECRET = os.getenv("DELEGATION_SECRET", "change-me")
ALGO = hashlib.sha256
DEFAULT_MINUTES = 10


def _sign(data: str) -> str:
    return hmac.new(SECRET.encode(), data.encode(), ALGO).hexdigest()


def create_token(
    user_id: str,
    agent_id: str,
    portal: str,
    minutes: int = DEFAULT_MINUTES,
) -> str:
    """Return a URL-safe signed token."""
    exp = (datetime.utcnow() + timedelta(minutes=minutes)).timestamp()
    payload = json.dumps({
        "user": user_id,
        "agent": agent_id,
        "portal": portal,
        "exp": exp,
    })
    data = base64.urlsafe_b64encode(payload.encode()).decode()
    return f"{data}.{_sign(payload)}"


def verify_token(token: str) -> Optional[Dict[str, str]]:
    """Validate ``token`` and return claims if valid."""
    try:
        data, sig = token.rsplit(".", 1)
        payload = base64.urlsafe_b64decode(data.encode()).decode()
        if _sign(payload) != sig:
            return None
        claims = json.loads(payload)
        if claims.get("exp", 0) < datetime.utcnow().timestamp():
            return None
        return claims
    except Exception:
        return None
