import json
import importlib
from pathlib import Path

from fastapi.testclient import TestClient


def test_log_event(monkeypatch, tmp_path):
    log_file = tmp_path / "audit.json"
    monkeypatch.setenv("AUDIT_LOG", str(log_file))
    audit = importlib.reload(importlib.import_module("app.storage.audit"))

    audit.log_event("alice", "scrape", {"portal": "portal1"})
    audit.log_event("bob", "login", {"portal": "portal2"})

    data = json.loads(log_file.read_text())
    assert len(data) == 2
    assert data[0]["user"] == "alice"
    assert data[0]["action"] == "scrape"
    assert data[0]["context"]["portal"] == "portal1"


def test_consent_endpoint(monkeypatch, tmp_path):
    log_file = tmp_path / "audit.json"
    monkeypatch.setenv("AUDIT_LOG", str(log_file))
    audit = importlib.reload(importlib.import_module("app.storage.audit"))
    consent = importlib.reload(importlib.import_module("app.api.consent"))

    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(consent.router)
    client = TestClient(app)

    payload = {
        "user_id": "user1",
        "portal_name": "MyChart",
        "action": "scrape",
        "timestamp": "2023-01-01T00:00:00",
    }
    resp = client.post("/consent", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"status": "consent recorded"}

    logs = json.loads(log_file.read_text())
    assert len(logs) == 1
    assert logs[0]["user"] == "user1"
    assert logs[0]["context"]["portal"] == "MyChart"
