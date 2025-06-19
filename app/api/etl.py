from __future__ import annotations

from datetime import datetime
import os
import logging

from fastapi import APIRouter, Form, Query, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse

from app.storage import blob, audit
logger = logging.getLogger(__name__)
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])

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
    logger.info("[/process] confirm for session %s with %d files", session_key, len(files))
    html = HTML_TEMPLATE.format(count=len(files), session_key=session_key)
    return HTMLResponse(content=html)



@router.post("/process")
def process_files(bg: BackgroundTasks, session_key: str = Form(...)) -> JSONResponse:
    """Run ETL pipeline after user confirmation."""
    logger.info("[/process] starting for session %s", session_key)
    audit.log_event(
        session_key,
        "consent_given",
        {"timestamp": datetime.utcnow().isoformat()},
    )
    if not _dry_run():
        from app.orchestrator import run_etl_from_blobs

        bg.add_task(run_etl_from_blobs, session_key)
        logger.info("[/process] ETL task queued for %s", session_key)
        status = "processing"
        message = (
            "Your files are being processed. Please check /summary later."
        )
    else:
        status = "dry-run"
        message = "DRY_RUN is enabled; ETL skipped."
        logger.info("[/process] dry run for session %s", session_key)

    return JSONResponse(
        {"status": status, "message": message, "session_key": session_key}
    )
