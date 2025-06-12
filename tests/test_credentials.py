import importlib
import os
import sys
import time
from pathlib import Path

import fakeredis
from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.storage import redis as redis_module


def _setup(monkeypatch):
    key = Fernet.generate_key()
    monkeypatch.setenv("FERNET_KEY", key.decode())
    redis_module._redis_client = fakeredis.FakeRedis(decode_responses=True)
    return importlib.reload(importlib.import_module("app.storage.credentials"))


def test_encrypt_decrypt_roundtrip(monkeypatch):
    creds = _setup(monkeypatch)

    creds.store_credentials("portal1", "alice", "secret")
    raw = redis_module.get_key("creds:portal1")
    assert raw and "secret" not in raw

    data = creds.get_credentials("portal1")
    assert data == {"username": "alice", "password": "secret"}


def test_ttl_expiry(monkeypatch):
    creds = _setup(monkeypatch)

    creds.TTL_SECONDS = 1
    creds.store_credentials("portal2", "bob", "pw")
    time.sleep(1.1)
    assert creds.get_credentials("portal2") is None


