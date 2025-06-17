import importlib
import os
import sys
from datetime import date
from pathlib import Path

from app.utils import llm


def _setup_db(tmp_path: Path, monkeypatch) -> Path:
    db_path = tmp_path / "sample.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()

    session = db_module.SessionLocal()
    session.add(
        models_module.LabResult(
            test_name="Cholesterol",
            value=5.8,
            units="mmol/L",
            date=date.fromisoformat("2023-05-01"),
        )
    )
    session.add(
        models_module.VisitSummary(
            provider="Clinic",
            doctor="Dr. Jones",
            notes="Routine",
            date=date.fromisoformat("2023-06-01"),
        )
    )
    session.add(
        models_module.StructuredRecord(
            portal="portal",
            type="note",
            text="Some note",
            source_url="url",
            session_key="sess",
        )
    )
    session.commit()
    session.close()
    return db_path


def test_ask_tool_cli(tmp_path, monkeypatch, capsys, caplog):
    db = _setup_db(tmp_path, monkeypatch)

    def fake_create(messages, **_kwargs):
        content = messages[0]["content"]
        assert "Cholesterol" in content
        assert "Clinic" in content
        assert "Some note" in content
        return "Mock answer"

    monkeypatch.setattr(llm, "chat_completion", fake_create)
    import scripts.ask_tool as ask_tool
    monkeypatch.setattr(ask_tool.llm, "chat_completion", fake_create)

    monkeypatch.setattr(
        sys,
        "argv",
        ["ask_tool.py", "--db", str(db), "--session", "sess", "--query", "How am I doing?"],
    )
    with caplog.at_level("INFO"):
        ask_tool.main()
    result = capsys.readouterr()
    logged = result.out + result.err + "\n".join(record.message for record in caplog.records)
    assert "Mock answer" in logged

    # reload DB modules to avoid affecting other tests
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    import app.storage.db as db_module
    import app.storage.models as models_module
    importlib.reload(db_module)
    importlib.reload(models_module)

