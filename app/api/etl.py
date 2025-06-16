from __future__ import annotations

from datetime import datetime
import os

from fastapi import APIRouter, Form, Query
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, JSONResponse

from app.storage import blob, audit

router = APIRouter()

HTML_TEMPLATE = (
    "<html><body>"
    "<p>You uploaded {count} files. Do you want to process them now?</p>"
    "<form method='post'>"
    "<input type='hidden' name='session_key' value='{session_key}'>"
    "<button type='submit'>Process</button>"
    "</form>"
    "</body></html>"
)


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

@router.get("/process", response_class=HTMLResponse)
def confirm_process(session_key: str = Query(...)) -> HTMLResponse:
    """Return confirmation prompt before running ETL."""
    files = blob.list_blobs(session_key)
    html = HTML_TEMPLATE.format(count=len(files), session_key=session_key)
    return HTMLResponse(content=html)



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
