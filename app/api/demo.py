from __future__ import annotations

import random
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.utils import generate_session_key
from app.storage import blob
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])

DEMO_DIR = Path(__file__).resolve().parents[2] / "project" / "demo_data"


@router.post("/load_demo")
def load_demo() -> JSONResponse:
    """Load a sample health record and run the ETL pipeline."""
    pdfs = list(DEMO_DIR.glob("*.pdf"))
    if not pdfs:
        raise HTTPException(status_code=500, detail="No demo data available")

    file_path = random.choice(pdfs)
    data = file_path.read_bytes()

    session_key = generate_session_key()
    blob_name = f"{session_key}/{file_path.name}"
    url = blob.upload_file_and_get_url(
        data, blob_name, content_type="application/pdf"
    )
    blob.record_upload(session_key, "demo", file_path.name)
    from app.orchestrator import run_etl_from_blobs

    run_etl_from_blobs(session_key)

    return JSONResponse(
        {"session_key": session_key, "source": file_path.name, "source_url": url}
    )
