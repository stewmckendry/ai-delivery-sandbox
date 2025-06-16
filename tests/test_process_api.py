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

    blob_module = importlib.import_module("app.storage.blob")
    monkeypatch.setattr(blob_module, "list_blobs", lambda prefix: [f"{prefix}/a.pdf", f"{prefix}/b.html"])

    called = {}
    monkeypatch.setattr(importlib.import_module("app.orchestrator"), "run_etl_from_blobs", lambda prefix: called.setdefault("prefix", prefix))

    etl_module = importlib.reload(importlib.import_module("app.api.etl"))
    app = FastAPI()
    app.include_router(etl_module.router)
    client = TestClient(app)
    return client, log_file, called


def test_process_route(monkeypatch, tmp_path):
    client, log_file, called = setup_app(monkeypatch, tmp_path)

    resp = client.get("/process", params={"session_key": "sess"})
    assert resp.status_code == 200
    assert "You uploaded 2 files" in resp.text

    resp = client.post("/process", data={"session_key": "sess"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "processing complete"
    assert called["prefix"] == "sess"

    logs = json.loads(log_file.read_text())
    assert logs and logs[0]["action"] == "consent_given"
