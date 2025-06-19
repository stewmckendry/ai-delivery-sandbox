import importlib
import random
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def setup_app(monkeypatch):
    monkeypatch.setenv("DELEGATION_SECRET", "test")
    from cryptography.fernet import Fernet
    monkeypatch.setenv("FERNET_KEY", Fernet.generate_key().decode())
    from app.auth.token import create_token
    token = create_token("user", "agent", "portal")

    demo_module = importlib.reload(importlib.import_module("app.api.demo"))

    sample = next((ROOT / "project" / "demo_data").glob("*.pdf"))
    monkeypatch.setattr(random, "choice", lambda seq: sample)
    monkeypatch.setattr(
        demo_module.blob,
        "upload_file_and_get_url",
        lambda data, name, **k: f"https://blob/{name}",
    )
    called = {}
    import app.orchestrator as orch_module
    monkeypatch.setattr(
        orch_module,
        "run_etl_from_blobs",
        lambda prefix: called.setdefault("prefix", prefix),
    )
    monkeypatch.setattr(demo_module, "generate_session_key", lambda: "sess")

    app = FastAPI()
    app.include_router(demo_module.router)
    client = TestClient(app)
    return client, token, called, sample.name


def test_load_demo(monkeypatch):
    client, token, called, filename = setup_app(monkeypatch)
    resp = client.post("/load_demo", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["session_key"] == "sess"
    assert body["source"] == filename
    assert body["source_url"].startswith("https://blob/sess/")
    assert called["prefix"] == "sess"
