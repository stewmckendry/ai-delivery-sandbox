import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient


def setup_app(monkeypatch):
    monkeypatch.setenv("DELEGATION_SECRET", "test")
    monkeypatch.setenv("CHROMA_OPENAI_API_KEY", "sk-test")
    from app.auth.token import create_token
    token = create_token("user", "agent", "portal")

    def fake_search(query, session_key, n_results=5):
        return [
            {"text": "Patient treated for sprained ankle", "type": "Procedure", "code": "6142004"},
            {"text": "Discharged with crutches"},
        ]

    def fake_chat(messages, **_kwargs):
        content = messages[0]["content"]
        assert "Record 1:" in content
        assert "Type: Procedure" in content
        assert "Code: 6142004" in content
        return "Vector answer"

    import app.rag.searcher as search_module
    monkeypatch.setattr(search_module, "search_records", fake_search)
    import app.api.rag as rag_module
    monkeypatch.setattr(rag_module, "chat_completion", fake_chat)

    import app.main as main_module
    main_module = importlib.reload(main_module)
    return TestClient(main_module.app), token


def test_ask_vector(monkeypatch):
    client, token = setup_app(monkeypatch)
    resp = client.post(
        "/ask_vector",
        json={"query": "test", "session_key": "sess"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"answer": "Vector answer"}
