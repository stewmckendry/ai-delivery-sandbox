from __future__ import annotations

import random
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.utils import generate_session_key
from app.storage import blob
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])

@router.post("/load_demo")
def load_demo() -> JSONResponse:
    """Load a sample health record from blob storage and run ETL."""
    try:
        demo_blobs = blob.list_demo_blob_files("demo/")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Demo storage not available") from exc
    if not demo_blobs:
        raise HTTPException(status_code=500, detail="No demo data available")

    blob_name = random.choice(demo_blobs)
    filename = Path(blob_name).name
    data = blob.download_blob(blob_name)

    session_key = generate_session_key()
    dest_name = f"{session_key}/{filename}"
    url = blob.upload_file_and_get_url(
        data, dest_name, content_type="application/pdf"
    )
    blob.record_upload(session_key, "demo", filename)
    from app.orchestrator import run_etl_from_blobs

    run_etl_from_blobs(session_key)

    return JSONResponse({"session_key": session_key, "source": filename, "source_url": url})
