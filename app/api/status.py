from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import logging
from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from app.storage import audit
from app.storage.db import SessionLocal, init_db
from app.storage import models
from sqlalchemy import func
from app.auth.token import require_token

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(require_token)])


def _load_audit(session_key: str) -> list[dict]:
    if not audit.AUDIT_PATH.exists():
        return []
    try:
        data = json.loads(Path(audit.AUDIT_PATH).read_text())
    except Exception:
        return []
    return [e for e in data if e.get("user") == session_key]


@router.get("/summary")
def summary(session_key: str = Query(...)) -> JSONResponse:
    """Return summary of uploaded and processed records for ``session_key``."""
    logger.info("[/summary] session=%s", session_key)
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
        labs = (
            session.query(models.LabResult)
            .filter(models.LabResult.session_key == session_key)
            .count()
        )
        visits = (
            session.query(models.VisitSummary)
            .filter(models.VisitSummary.session_key == session_key)
            .count()
        )
        structured = (
            session.query(models.StructuredRecord)
            .filter(models.StructuredRecord.session_key == session_key)
            .count()
        )
        logger.info(
            "[/summary] uploads=%d labs=%d visits=%d structured=%d",
            len(uploads),
            labs,
            visits,
            structured,
        )
        latest_times = []
        lab_last = (
            session.query(models.LabResult)
            .filter(models.LabResult.session_key == session_key)
            .order_by(models.LabResult.date.desc())
            .first()
        )
        lab_date = lab_last.date.isoformat() if lab_last else None
        if lab_date:
            latest_times.append(lab_date)
        visit_last = (
            session.query(models.VisitSummary)
            .filter(models.VisitSummary.session_key == session_key)
            .order_by(models.VisitSummary.date.desc())
            .first()
        )
        visit_date = visit_last.date.isoformat() if visit_last else None
        if visit_date:
            latest_times.append(visit_date)
        struct_last = (
            session.query(models.StructuredRecord)
            .filter(models.StructuredRecord.session_key == session_key)
            .order_by(models.StructuredRecord.date_created.desc())
            .first()
        )
        struct_date = (
            struct_last.date_created.isoformat() if struct_last else None
        )
        if struct_date:
            latest_times.append(struct_date)
    finally:
        session.close()

    latest_processing = max(latest_times) if latest_times else None

    type_counts = (
        session.query(models.StructuredRecord.clinical_type, func.count())
        .filter(models.StructuredRecord.session_key == session_key)
        .group_by(models.StructuredRecord.clinical_type)
        .all()
    )
    clinical_breakdown = {t or "unknown": c for t, c in type_counts}

    resp = {
        "uploads": uploads,
        "record_counts": {
            "labs": labs,
            "visits": visits,
            "structured": structured,
            "by_clinical_type": clinical_breakdown,
        },
        "latest_upload": latest_upload,
        "latest_processing": latest_processing,
        "latest_record_dates": {
            "labs": lab_date,
            "visits": visit_date,
            "structured": struct_date,
        },
    }
    structured_rows = (
        session.query(models.StructuredRecord)
        .filter(models.StructuredRecord.session_key == session_key)
        .order_by(models.StructuredRecord.date_created)
        .all()
    )
    resp["structured_records"] = [
        {
            "portal": r.portal,
            "type": r.type,
            "clinical_type": r.clinical_type,
            "code": r.code,
            "code_system": r.code_system,
            "display": r.display,
            "source_url": r.source_url,
            "timestamp": r.date_created.isoformat(),
            "duplicate": bool(getattr(r, "is_duplicate", False)),
        }
        for r in structured_rows
    ]
    if not uploads and not any([labs, visits, structured]):
        logger.error("[/summary] no records found for session %s", session_key)
        resp[
            "message"
        ] = (
            "No records found. Visit /upload or /process to add data. "
            "If Operator is blocked by reCAPTCHA or Cloudflare, save the page "
            "as HTML or PDF and upload it manually."
        )
    else:
        if labs == 0:
            logger.error("[/summary] no lab results for session %s", session_key)
        if visits == 0:
            logger.error("[/summary] no visit summaries for session %s", session_key)
        if structured == 0:
            logger.error("[/summary] no structured records for session %s", session_key)
    return JSONResponse(resp)
