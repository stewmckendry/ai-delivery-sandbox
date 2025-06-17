import os
import importlib
from datetime import date
import tempfile

from fastapi.testclient import TestClient
from app.utils import llm


def setup_app(labs, visits, monkeypatch):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp.name}"
    # Reload db and models to use new DB URL
    import app.storage.db as db_module
    import app.storage.models as models_module
    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()

    session = db_module.SessionLocal()
    for lab in labs:
        session.add(models_module.LabResult(**lab))
    for visit in visits:
        session.add(models_module.VisitSummary(**visit))
    session.commit()
    session.close()

    def fake_create(messages, **_kwargs):
        content = messages[0]["content"]
        # Ensure context is included
        for lab in labs:
            assert lab["test_name"] in content
        for visit in visits:
            assert visit["provider"] in content
        return "Mock answer"
    monkeypatch.setattr(llm, "chat_completion", fake_create)
    import app.api.rag as rag_module
    monkeypatch.setattr(rag_module, "chat_completion", fake_create)

    import app.main as main_module
    main_module = importlib.reload(main_module)
    return TestClient(main_module.app), tmp.name


def test_ask_endpoint(monkeypatch):
    labs = [
        {
            "test_name": "Cholesterol",
            "value": 5.8,
            "units": "mmol/L",
            "date": date.fromisoformat("2023-05-01"),
            "session_key": "sess",
        }
    ]
    visits = [
        {
            "date": date.fromisoformat("2023-06-01"),
            "provider": "General Hospital",
            "doctor": "Dr. Jones",
            "notes": "Routine check",
            "session_key": "sess",
        }
    ]

    client, path = setup_app(labs, visits, monkeypatch)
    resp = client.post("/ask", json={"query": "How am I doing?", "session_key": "sess"})
    assert resp.status_code == 200
    assert resp.json() == {"answer": "Mock answer"}
    os.unlink(path)

