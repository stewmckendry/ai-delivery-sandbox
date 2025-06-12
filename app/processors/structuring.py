"""Utilities for inserting structured data into the database."""

from __future__ import annotations

from datetime import date
from typing import List, Dict

from sqlalchemy.orm import Session

from app.storage.models import LabResult, VisitSummary


def _parse_date(value: str | date) -> date:
    """Convert an ISO date string or ``date`` into ``date``."""
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def insert_lab_results(session: Session, results: List[Dict]):
    """Convert ``results`` to ``LabResult`` objects and save them."""
    objects = []
    for entry in results:
        if not entry.get("date"):
            # Skip entries without a valid date since column is non-nullable
            continue
        lab = LabResult(
            test_name=entry["test_name"],
            value=float(entry["value"]),
            units=entry["units"],
            date=_parse_date(entry["date"]),
        )
        objects.append(lab)
    session.add_all(objects)
    session.commit()


def insert_visit_summaries(session: Session, summaries: List[Dict]):
    """Convert ``summaries`` to ``VisitSummary`` objects and save them."""
    objects = []
    for entry in summaries:
        if not entry.get("date"):
            continue
        visit = VisitSummary(
            provider=entry["provider"],
            doctor=entry["doctor"],
            notes=entry["notes"],
            date=_parse_date(entry["date"]),
        )
        objects.append(visit)
    session.add_all(objects)
    session.commit()
