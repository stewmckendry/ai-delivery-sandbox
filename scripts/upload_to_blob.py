#!/usr/bin/env python
"""Upload a local file to Azure Blob Storage for ETL processing."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
import httpx

# Load environment variables from .env if present
load_dotenv()

# Ensure repo root is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.storage import blob


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload file to Azure Blob")
    parser.add_argument("--session-key", required=True, help="Session identifier")
    parser.add_argument("--file", required=True, help="Path to local file")
    parser.add_argument("--portal", default="", help="Portal name for metadata")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return

    url = blob.generate_upload_url(args.session_key, file_path.name)

    with file_path.open("rb") as fh:
        resp = httpx.put(url, data=fh.read())
    resp.raise_for_status()

    blob.record_upload(args.session_key, args.portal, file_path.name)

    blob_path = f"{args.session_key}/{file_path.name}"
    print(f"Uploaded {file_path} to {blob_path} (status {resp.status_code})")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
