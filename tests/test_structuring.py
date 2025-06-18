import os
import importlib

from app.processors.structuring import insert_lab_results, insert_visit_summaries
from app.storage.structured import insert_structured_records


def test_insert_functions():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    import app.storage.db as db_module
    import app.storage.models as models_module
    db_module = importlib.reload(db_module)
    models = importlib.reload(models_module)

    db_module.init_db()
    session = db_module.SessionLocal()

    lab_data = [
        {"test_name": "Cholesterol", "value": "5.8", "units": "mmol/L", "date": "2023-05-01"},
        {"test_name": "Hemoglobin", "value": "13.5", "units": "g/dL", "date": "2023-05-02"},
    ]
    insert_lab_results(session, lab_data, session_key="sess")

    visit_data = [
        {"date": "2023-06-01", "provider": "General Hospital", "doctor": "Dr. Jones", "notes": "Follow-up"},
        {"date": "2023-07-10", "provider": "City Clinic", "doctor": "Dr. Smith", "notes": "All good."},
    ]
    insert_visit_summaries(session, visit_data, session_key="sess")

    labs = (
        session.query(models.LabResult)
        .filter(models.LabResult.session_key == "sess")
        .order_by(models.LabResult.id)
        .all()
    )
    visits = (
        session.query(models.VisitSummary)
        .filter(models.VisitSummary.session_key == "sess")
        .order_by(models.VisitSummary.id)
        .all()
    )

    assert len(labs) == 2
    assert labs[0].test_name == "Cholesterol"
    assert labs[0].value == 5.8
    assert labs[1].units == "g/dL"

    assert len(visits) == 2
    assert visits[0].provider == "General Hospital"
    assert visits[1].notes == "All good."

    session.close()


def test_insert_structured_records():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()

    records = [
        {"portal": "portal_a", "type": "visit", "text": "hello", "source_url": "url1"},
        {"portal": "portal_a", "type": "lab", "text": "bye", "source_url": "url2"},
    ]
    insert_structured_records(session, records, session_key="sess")

    saved = session.query(models_module.StructuredRecord).all()
    assert len(saved) == 2
    assert saved[0].text == "hello"
    assert saved[0].source == "operator"
    assert saved[0].session_key == "sess"
    assert hasattr(saved[0], "capture_method")
    assert hasattr(saved[0], "clinical_type")
    session.close()


def test_deduplication_flag():
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    session = db_module.SessionLocal()

    records = [
        {
            "portal": "portal_a",
            "type": "visit",
            "text": "hello",
            "source_url": "url1",
        },
        {
            "portal": "portal_a",
            "type": "visit",
            "text": "hello",
            "source_url": "url1",
        },
    ]
    insert_structured_records(session, records, session_key="sess")

    saved = (
        session.query(models_module.StructuredRecord)
        .filter(models_module.StructuredRecord.session_key == "sess")
        .order_by(models_module.StructuredRecord.id)
        .all()
    )
    assert len(saved) == 2
    assert saved[0].is_duplicate is False
    assert saved[1].is_duplicate is True
    session.close()
