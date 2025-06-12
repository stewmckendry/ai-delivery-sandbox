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
    )
    visit = models.VisitSummary(
        provider="City Hospital",
        doctor="Dr. Smith",
        notes="Routine checkup",
        date=date.today(),
    )

    session.add(lab)
    session.add(visit)
    session.commit()

    labs = session.query(models.LabResult).all()
    visits = session.query(models.VisitSummary).all()

    assert len(labs) == 1
    assert labs[0].test_name == "Hemoglobin"
    assert len(visits) == 1
    assert visits[0].doctor == "Dr. Smith"

    session.close()
