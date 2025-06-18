import importlib
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def setup_app(monkeypatch, tmp_path):
    db_path = tmp_path / "db.sqlite"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()
    session.add(
        models_module.StructuredRecord(
            portal="portal1",
            type="note",
            text="note",
            source_url="",
            session_key="sess",
        )
    )
    session.commit()
    session.close()

    monkeypatch.setenv("DELEGATION_SECRET", "test")
    from app.auth.token import create_token
    token = create_token("user", "agent", "portal")

    called = {}

    def fake_upload(data, name, ttl_minutes=30):
        called["data"] = data
        called["name"] = name
        return f"https://blob/{name}"

    blob_module = importlib.import_module("app.storage.blob")
    monkeypatch.setattr(blob_module, "upload_file_and_get_url", fake_upload)

    export_module = importlib.reload(importlib.import_module("app.api.export"))
    app = FastAPI()
    app.include_router(export_module.router)
    client = TestClient(app)
    return client, token, called


def test_export_returns_blob_url(monkeypatch, tmp_path):
    client, token, called = setup_app(monkeypatch, tmp_path)

    resp = client.get(
        "/export",
        params={"session_key": "sess", "format": "markdown"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["download_url"] == f"https://blob/{called['name']}"
    assert "Structured Records" in called["data"]


def test_export_pdf_upload(monkeypatch, tmp_path):
    client, token, called = setup_app(monkeypatch, tmp_path)

    resp = client.get(
        "/export",
        params={"session_key": "sess", "format": "pdf"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["download_url"] == f"https://blob/{called['name']}"
    assert called["name"].endswith(".pdf")
