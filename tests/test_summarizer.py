import os
import importlib
from datetime import date

from app.prompts.summarizer import summarize_blocks, summarize_database_records
from app.utils import llm


def test_summarize_blocks(monkeypatch):
    # Prepare fake response
    def fake_create(messages, **_kwargs):
        return "Summary text"

    monkeypatch.setattr(llm, "chat_completion", fake_create)
    import app.prompts.summarizer as summarizer_module
    monkeypatch.setattr(summarizer_module, "chat_completion", fake_create)

    blocks = [
        {"text": "Patient reports mild headache."},
        {"text": "Blood pressure within normal range."},
    ]

    summary = summarize_blocks(blocks)
    assert summary == "Summary text"


def test_summarize_database_records(monkeypatch):
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()

    session.add(
        models_module.VisitSummary(
            provider="Clinic",
            doctor="Dr. A",
            notes="Checkup",
            date=date.fromisoformat("2023-01-01"),
        )
    )
    session.add(
        models_module.VisitSummary(
            provider="Clinic",
            doctor="Dr. B",
            notes="Follow-up",
            date=date.fromisoformat("2023-01-02"),
        )
    )
    session.add(
        models_module.LabResult(
            test_name="Cholesterol",
            value=180,
            units="mg/dL",
            date=date.fromisoformat("2023-01-03"),
        )
    )
    session.add(
        models_module.LabResult(
            test_name="Glucose",
            value=95,
            units="mg/dL",
            date=date.fromisoformat("2023-01-04"),
        )
    )
    session.add(
        models_module.StructuredRecord(
            portal="portal",
            type="note",
            text="Some structured note",
            source_url="url",
        )
    )
    session.commit()

    def fake_create(messages, **_kwargs):
        return "LLM summary"

    monkeypatch.setattr(llm, "chat_completion", fake_create)
    import app.prompts.summarizer as summarizer_module
    monkeypatch.setattr(summarizer_module, "chat_completion", fake_create)

    summary = summarize_database_records(session)
    assert summary.startswith("###")
    assert "2 visits" in summary
    assert "2 lab results" in summary
    assert "LLM summary" in summary

    session.close()
