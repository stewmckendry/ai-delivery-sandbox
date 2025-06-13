from __future__ import annotations

from sqlalchemy.orm import Session

from .models import StructuredRecord


def insert_structured_records(session: Session, records: list[dict]) -> None:
    """Insert cleaned AI-extracted records."""
    objs = [StructuredRecord(**r) for r in records]
    session.add_all(objs)
    session.commit()
