import json
import importlib
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def setup_app(monkeypatch, tmp_path):
    log_file = tmp_path / "audit.json"
    monkeypatch.setenv("AUDIT_LOG", str(log_file))
    from cryptography.fernet import Fernet
    monkeypatch.setenv("FERNET_KEY", Fernet.generate_key().decode())
    importlib.reload(importlib.import_module("app.storage.audit"))

    monkeypatch.setenv("DELEGATION_SECRET", "test")
    from app.auth.token import create_token
    token = create_token("user", "agent", "portal")

    blob_module = importlib.import_module("app.storage.blob")
    monkeypatch.setattr(blob_module, "list_blobs", lambda prefix: [f"{prefix}/a.pdf", f"{prefix}/b.html"])

    called = {}
    def fake_run(prefix):
        called.setdefault("prefix", prefix)
        return "sum"

    monkeypatch.setattr(importlib.import_module("app.orchestrator"), "run_etl_from_blobs", fake_run)

    etl_module = importlib.reload(importlib.import_module("app.api.etl"))
    app = FastAPI()
    app.include_router(etl_module.router)
    client = TestClient(app)
    return client, log_file, called, token


def test_process_flow(monkeypatch, tmp_path):
    client, log_file, called, token = setup_app(monkeypatch, tmp_path)

    resp = client.get(
        "/status", params={"session_key": "sess"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert "You\'ve uploaded 2 files" in resp.json()["prompt"]
    
def test_process_route(monkeypatch, tmp_path):
    client, log_file, called, token = setup_app(monkeypatch, tmp_path)

    resp = client.get(
        "/process", params={"session_key": "sess"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert "You uploaded 2 files" in resp.text


    resp = client.post(
        "/process",
        data={"session_key": "sess"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "processing"
    assert body["session_key"] == "sess"
    assert "check /summary" in body["message"]
    assert called["prefix"] == "sess"

    logs = json.loads(log_file.read_text())
    assert logs and logs[0]["action"] == "consent_given"
