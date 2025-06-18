import importlib

from fastapi import FastAPI
from fastapi.testclient import TestClient


def setup_app(monkeypatch):
    monkeypatch.setenv("DELEGATION_SECRET", "test")
    token_module = importlib.import_module("app.auth.token")
    token = token_module.create_token("user", "agent", "portal")

    session_module = importlib.reload(importlib.import_module("app.api.session"))
    app = FastAPI()
    app.include_router(session_module.router)
    client = TestClient(app)
    return client, token


def test_session_endpoint(monkeypatch):
    client, token = setup_app(monkeypatch)
    resp1 = client.get("/session", headers={"Authorization": f"Bearer {token}"})
    resp2 = client.get("/session", headers={"Authorization": f"Bearer {token}"})
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    key1 = resp1.json().get("session_key")
    key2 = resp2.json().get("session_key")
    assert isinstance(key1, str) and len(key1) >= 32
    assert key1 != key2
