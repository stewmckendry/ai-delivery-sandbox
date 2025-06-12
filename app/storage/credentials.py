from __future__ import annotations

import json
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from cryptography.fernet import Fernet

from . import redis as redis_store

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY environment variable is required")

_f = Fernet(FERNET_KEY.encode() if isinstance(FERNET_KEY, str) else FERNET_KEY)

PREFIX = "creds"
TTL_SECONDS = 600  # 10 minutes


def _make_key(portal: str) -> str:
    return f"{PREFIX}:{portal}"


def store_credentials(portal: str, username: str, password: str) -> bool:
    """Encrypt ``password`` and store credentials in Redis with TTL."""
    data = {
        "username": username,
        "password": _f.encrypt(password.encode()).decode(),
    }
    return redis_store.set_key(_make_key(portal), json.dumps(data), expire=TTL_SECONDS)


def get_credentials(portal: str) -> Optional[Dict[str, str]]:
    """Retrieve and decrypt credentials for ``portal``."""
    raw = redis_store.get_key(_make_key(portal))
    if not raw:
        return None
    data = json.loads(raw)
    password = _f.decrypt(data["password"].encode()).decode()
    return {"username": data["username"], "password": password}


def delete_credentials(portal: str) -> int:
    """Delete stored credentials for ``portal``."""
    return redis_store.delete_key(_make_key(portal))
