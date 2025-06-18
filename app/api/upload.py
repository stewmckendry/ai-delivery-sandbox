from __future__ import annotations

from pathlib import Path
from fastapi import APIRouter, HTTPException, Query, Depends
import re
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse

from app.storage import blob
from app.auth.token import require_token

router = APIRouter()

HTML_PATH = Path(__file__).resolve().parents[1] / "web" / "upload_form.html"


@router.get("/upload", response_class=HTMLResponse)
def upload_form() -> HTMLResponse:
    """Serve the file upload HTML page."""
    html = HTML_PATH.read_text(encoding="utf-8")
    return HTMLResponse(html)


@router.get("/upload/sas", dependencies=[Depends(require_token)])
def get_sas(session_key: str = Query(...), filename: str = Query(...)) -> JSONResponse:
    """Return a SAS URL for uploading ``filename``."""
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in {"pdf", "html", "txt"}:
        raise HTTPException(status_code=400, detail="Invalid file type")
    url = blob.generate_upload_url(session_key, filename)
    return JSONResponse({"url": url})


@router.get("/upload/proxy_sas")
def get_proxy_sas(session_key: str = Query(...), filename: str = Query(...)) -> JSONResponse:
    """Public SAS generator restricted to safe filenames."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{3,64}", session_key or ""):
        raise HTTPException(status_code=400, detail="Invalid session key")
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in {"pdf", "html", "txt"}:
        raise HTTPException(status_code=400, detail="Invalid file type")
    url = blob.generate_upload_url(session_key, filename)
    return JSONResponse({"url": url})


@router.post("/upload/log", dependencies=[Depends(require_token)])
def log_upload(session_key: str, portal: str = "", filename: str = "") -> JSONResponse:
    """Record upload metadata via audit log."""
    blob.record_upload(session_key, portal, filename)
    return JSONResponse({"status": "logged"})
