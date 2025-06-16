from __future__ import annotations

from datetime import datetime
import os

from fastapi import APIRouter, Form, Query
from fastapi.responses import JSONResponse

from app.storage import blob, audit

router = APIRouter()

def _dry_run() -> bool:
    return os.getenv("DRY_RUN", "0").lower() in {"1", "true", "yes"}


@router.get("/status")
def upload_status(session_key: str = Query(...)) -> JSONResponse:
    """Return prompt asking to start analysis for uploaded files."""
    files = blob.list_blobs(session_key)
    if not files:
        return JSONResponse({"prompt": ""})
    msg = f"You've uploaded {len(files)} files. Would you like to analyze them now?"
    return JSONResponse({"prompt": msg})


@router.post("/process")
def process_files(session_key: str = Form(...)) -> JSONResponse:
    """Run ETL pipeline after user confirmation."""
    audit.log_event(session_key, "consent_given", {"timestamp": datetime.utcnow().isoformat()})
    if not _dry_run():
        from app.orchestrator import run_etl_from_blobs
        run_etl_from_blobs(session_key)
        status = "processing complete"
    else:
        status = "dry-run"
    return JSONResponse({"status": status})
