import os
import importlib
import json
import sys
from pathlib import Path
from datetime import date
from fastapi.testclient import TestClient
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def setup_app(monkeypatch, tmp_path):
    log_file = tmp_path / "audit.json"
    monkeypatch.setenv("AUDIT_LOG", str(log_file))
    audit = importlib.reload(importlib.import_module("app.storage.audit"))
    audit.log_event(
        "sess",
        "file_upload",
        {"portal": "portal1", "filename": "a.pdf", "timestamp": "2025-01-01T00:00:00"},
    )
    audit.log_event(
        "sess",
        "file_upload",
        {"portal": "portal1", "filename": "b.html", "timestamp": "2025-01-02T00:00:00"},
    )

    db_path = tmp_path / "db.sqlite"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()
    session.add(
        models_module.LabResult(
            test_name="Chol", value=5.0, units="mmol", date=date.today()
        )
    )
    session.add(
        models_module.VisitSummary(
            provider="Clinic", doctor="Dr. X", notes="hi", date=date.today()
        )
    )
    session.add(
        models_module.StructuredRecord(
            portal="portal1", type="note", text="note", source_url="src", session_key="sess"
        )
    )
    session.commit()
    session.close()

    status_module = importlib.reload(importlib.import_module("app.api.status"))
    app = FastAPI()
    app.include_router(status_module.router)
    client = TestClient(app)
    return client


def test_status_endpoint(monkeypatch, tmp_path):
    client = setup_app(monkeypatch, tmp_path)
    resp = client.get("/status", params={"session_key": "sess"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["uploads"]) == 2
    assert data["record_counts"]["labs"] == 1
    assert data["record_counts"]["visits"] == 1
    assert data["record_counts"]["structured"] == 1
