import importlib
from fastapi import FastAPI
from fastapi.testclient import TestClient


def setup_app(monkeypatch=None):
    upload_module = importlib.reload(importlib.import_module("app.api.upload"))
    app = FastAPI()
    app.include_router(upload_module.router)
    if monkeypatch:
        monkeypatch.setattr(
            upload_module.blob,
            "generate_upload_url",
            lambda s, f: f"https://blob/{s}/{f}",
        )
    client = TestClient(app)
    return client


def test_upload_form_public_access():
    client = setup_app()
    resp = client.get("/upload", params={"session": "sess"})
    assert resp.status_code == 200
    assert "Upload Files" in resp.text


def test_proxy_sas_public(monkeypatch):
    client = setup_app(monkeypatch)
    resp = client.get("/upload/proxy_sas", params={"session_key": "sess", "filename": "test.pdf"})
    assert resp.status_code == 200
    assert resp.json()["url"] == "https://blob/sess/test.pdf"


def test_sas_requires_auth(monkeypatch):
    client = setup_app(monkeypatch)
    resp = client.get("/upload/sas", params={"session_key": "sess", "filename": "a.pdf"})
    assert resp.status_code == 422

