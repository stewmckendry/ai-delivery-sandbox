import os
from datetime import date

import pytest

# Use in-memory SQLite for tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.storage import db  # noqa: E402
from app.storage import models  # noqa: E402


def test_table_creation_and_insertion():
    db.init_db()
    session = db.SessionLocal()

    lab = models.LabResult(
        test_name="Hemoglobin",
        value=13.5,
        units="g/dL",
        date=date.today(),
        loinc_code="1234-5",
    )
    visit = models.VisitSummary(
        provider="City Hospital",
        doctor="Dr. Smith",
        notes="Routine checkup",
        date=date.today(),
        snomed_code="11110000",
    )

    session.add(lab)
    session.add(visit)
    session.commit()

    fhir = models.FHIRResource(
        resource_type="Observation",
        resource_json="{}",
        record_type="lab",
        record_id=lab.id,
    )
    session.add(fhir)
    session.commit()

    labs = session.query(models.LabResult).all()
    visits = session.query(models.VisitSummary).all()

    assert len(labs) == 1
    assert labs[0].test_name == "Hemoglobin"
    assert labs[0].loinc_code == "1234-5"
    assert len(visits) == 1
    assert visits[0].doctor == "Dr. Smith"
    assert visits[0].snomed_code == "11110000"

    fhir_rows = session.query(models.FHIRResource).all()
    assert len(fhir_rows) == 1
    assert fhir_rows[0].record_id == lab.id

    session.close()
