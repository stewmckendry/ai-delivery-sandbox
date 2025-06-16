from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.storage import audit
from app.storage.db import SessionLocal, init_db
from app.storage import models

router = APIRouter()


def _load_audit(session_key: str) -> list[dict]:
    if not audit.AUDIT_PATH.exists():
        return []
    try:
        data = json.loads(Path(audit.AUDIT_PATH).read_text())
    except Exception:
        return []
    return [e for e in data if e.get("user") == session_key]


@router.get("/status")
def status(session_key: str = Query(...)) -> JSONResponse:
    """Return summary of uploaded and processed records for ``session_key``."""
    entries = _load_audit(session_key)
    uploads = [
        {
            "filename": e["context"].get("filename", ""),
            "portal": e["context"].get("portal", ""),
            "timestamp": e["context"].get("timestamp", e.get("timestamp")),
        }
        for e in entries
        if e.get("action") == "file_upload"
    ]
    latest_upload = None
    if uploads:
        latest_upload = max(u.get("timestamp") for u in uploads)

    init_db()
    session = SessionLocal()
    try:
        labs = session.query(models.LabResult).count()
        visits = session.query(models.VisitSummary).count()
        structured = session.query(models.StructuredRecord).count()
        latest_times = []
        lab_last = (
            session.query(models.LabResult)
            .order_by(models.LabResult.date.desc())
            .first()
        )
        if lab_last:
            latest_times.append(lab_last.date.isoformat())
        visit_last = (
            session.query(models.VisitSummary)
            .order_by(models.VisitSummary.date.desc())
            .first()
        )
        if visit_last:
            latest_times.append(visit_last.date.isoformat())
        struct_last = (
            session.query(models.StructuredRecord)
            .order_by(models.StructuredRecord.date_created.desc())
            .first()
        )
        if struct_last:
            latest_times.append(struct_last.date_created.isoformat())
    finally:
        session.close()

    latest_processing = max(latest_times) if latest_times else None

    resp = {
        "uploads": uploads,
        "record_counts": {
            "labs": labs,
            "visits": visits,
            "structured": structured,
        },
        "latest_upload": latest_upload,
        "latest_processing": latest_processing,
    }
    if not uploads and not any([labs, visits, structured]):
        resp["message"] = "No records found. Visit /upload or /process to add data."
    return JSONResponse(resp)
