from __future__ import annotations

from sqlalchemy.orm import Session

from .models import StructuredRecord


def insert_structured_records(
    session: Session, records: list[dict], session_key: str | None = None
) -> None:
    """Insert cleaned AI-extracted records."""
    objs = []
    for rec in records:
        data = {
            "source": "operator",
            "capture_method": "",
            "user_notes": "",
            "session_key": session_key,
        }
        data.update(rec)
        objs.append(StructuredRecord(**data))
    session.add_all(objs)
    session.commit()
