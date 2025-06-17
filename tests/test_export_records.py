import importlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import export_records
from app.processors.structuring import insert_lab_results, insert_visit_summaries
from app.storage.structured import insert_structured_records


def _setup_db(tmp_path: Path, monkeypatch) -> Path:
    db_path = tmp_path / "sample.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()

    insert_lab_results(
        session,
        [
            {
                "test_name": "Cholesterol",
                "value": 5.8,
                "units": "mmol/L",
                "date": "2023-05-01",
            }
        ],
    )
    insert_visit_summaries(
        session,
        [
            {
                "provider": "Clinic",
                "doctor": "Dr. Jones",
                "notes": "Routine",
                "date": "2023-06-01",
            }
        ],
    )
    insert_structured_records(
        session,
        [
            {
                "portal": "test_portal",
                "type": "note",
                "text": "Some note",
                "source_url": "url",
                "session_key": "sess",
            }
        ],
        session_key="sess",
    )
    session.close()
    return db_path


def test_export_records_all_formats(tmp_path, monkeypatch):
    db = _setup_db(tmp_path, monkeypatch)
    out_json = tmp_path / "out.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "export_records.py",
            "--db",
            str(db),
            "--session",
            "sess",
            "--output",
            str(out_json),
        ],
    )
    export_records.main()
    data = json.loads(out_json.read_text())
    assert data["lab_results"][0]["test_name"] == "Cholesterol"

    out_md = tmp_path / "out.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "export_records.py",
            "--db",
            str(db),
            "--session",
            "sess",
            "--format",
            "markdown",
            "--output",
            str(out_md),
        ],
    )
    export_records.main()
    text = out_md.read_text()
    assert "## Lab Results" in text

    out_pdf = tmp_path / "out.pdf"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "export_records.py",
            "--db",
            str(db),
            "--session",
            "sess",
            "--format",
            "pdf",
            "--output",
            str(out_pdf),
        ],
    )
    export_records.main()
    assert out_pdf.exists() and out_pdf.stat().st_size > 0

    # reload DB modules to avoid affecting other tests
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    import app.storage.db as db_module
    import app.storage.models as models_module
    importlib.reload(db_module)
    importlib.reload(models_module)
