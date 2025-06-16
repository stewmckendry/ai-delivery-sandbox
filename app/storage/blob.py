from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas,
)
from azure.storage.blob._shared.base_client import parse_connection_str

from . import audit

# Load environment variables from .env if present
from dotenv import load_dotenv
load_dotenv()

CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER = os.getenv("BLOB_CONTAINER", "uploads")

if CONN_STR:
    _service = BlobServiceClient.from_connection_string(CONN_STR)
    _container = _service.get_container_client(CONTAINER)
    try:
        _container.get_container_properties()
    except Exception:
        _container.create_container()

    _primary, _secondary, _cred = parse_connection_str(CONN_STR, None, "blob")
    if isinstance(_cred, dict):
        _account_name = _cred["account_name"]
        _account_key = _cred["account_key"]
    else:
        _account_name = _service.account_name
        _account_key = None
else:
    _service = _container = None
    _account_name = _account_key = None


def generate_upload_url(session_key: str, filename: str, ttl_minutes: int = 15) -> str:
    """Return SAS URL for uploading ``filename`` in ``session_key`` folder."""
    if not _service or not _account_key:
        raise RuntimeError("Azure blob storage not configured")

    blob_name = f"{session_key}/{filename}"
    sas = generate_blob_sas(
        account_name=_account_name,
        container_name=CONTAINER,
        blob_name=blob_name,
        account_key=_account_key,
        permission=BlobSasPermissions(write=True, create=True),
        expiry=datetime.utcnow() + timedelta(minutes=ttl_minutes),
    )
    return f"{_container.url}/{blob_name}?{sas}"


def record_upload(session_key: str, portal: str, filename: str) -> None:
    """Log upload metadata to audit log."""
    audit.log_event(
        session_key,
        "file_upload",
        {"portal": portal, "filename": filename, "timestamp": datetime.utcnow().isoformat()},
    )


def list_blobs(prefix: str) -> list[str]:
    """Return blob names starting with ``prefix``."""
    if not _container:
        raise RuntimeError("Azure blob storage not configured")
    return [b.name for b in _container.list_blobs(name_starts_with=prefix)]


def list_blob_info(prefix: str) -> list[dict[str, object]]:
    """Return metadata for blobs with ``prefix``.

    Each result includes ``name``, ``last_modified`` and ``age_hours``.
    """
    if not _container:
        raise RuntimeError("Azure blob storage not configured")

    info: list[dict[str, object]] = []
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    for b in _container.list_blobs(name_starts_with=prefix):
        last = getattr(b, "last_modified", now)
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        age = (now - last).total_seconds() / 3600
        info.append({"name": b.name, "last_modified": last, "age_hours": age})
    return info


def download_blob(name: str) -> bytes:
    """Return contents of blob ``name``."""
    if not _container:
        raise RuntimeError("Azure blob storage not configured")
    client = _container.get_blob_client(name)
    stream = client.download_blob()
    return stream.readall()


def delete_blob(name: str) -> None:
    """Delete blob ``name`` if it exists."""
    if not _container:
        return
    try:
        _container.delete_blob(name)
    except Exception:
        pass
