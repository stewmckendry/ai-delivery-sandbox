from __future__ import annotations

from sqlalchemy.orm import Session

from .models import StructuredRecord, FHIRResource


def insert_structured_records(
    session: Session, records: list[dict], session_key: str | None = None
) -> None:
    """Insert cleaned AI-extracted records."""
    objs = []
    existing = {
        (r.text, r.source_url)
        for r in session.query(StructuredRecord)
        .filter(StructuredRecord.session_key == session_key)
        .all()
    }
    for rec in records:
        data = {
            "source": "operator",
            "capture_method": "",
            "user_notes": "",
            "session_key": session_key,
        }
        data.update(rec)
        key = (data.get("text"), data.get("source_url", ""))
        if key in existing:
            data["is_duplicate"] = True
        else:
            existing.add(key)
        objs.append(StructuredRecord(**data))
    if objs:
        session.add_all(objs)
        session.commit()


def insert_fhir_resources(session: Session, resources: list[dict]) -> None:
    """Save FHIR resources to the database."""
    objs = [FHIRResource(**res) for res in resources]
    if objs:
        session.add_all(objs)
        session.commit()
