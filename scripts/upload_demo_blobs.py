#!/usr/bin/env python
"""Upload local demo PDFs to Azure Blob Storage.

Run from the repo root:

    python scripts/upload_demo_blobs.py [--data-dir project/demo_data]

The script uploads ``*.pdf`` files under ``--data-dir`` to ``demo/`` in blob
storage. Existing blobs are skipped unless ``--force`` is provided.
Ensure ``AZURE_STORAGE_CONNECTION_STRING`` is configured via environment or
``.env``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.storage import blob


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload demo PDFs to blob")
    parser.add_argument(
        "--data-dir",
        default=str(ROOT_DIR / "project" / "demo_data"),
        help="Directory containing demo PDF files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing blobs instead of skipping",
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.is_dir():
        print(f"ERROR: {data_dir} does not exist")
        return

    try:
        existing = set(blob.list_demo_blob_files("demo/"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: cannot list demo blobs: {exc}")
        return

    uploaded = 0
    for path in sorted(data_dir.glob("*.pdf")):
        blob_name = f"demo/{path.name}"
        if blob_name in existing and not args.force:
            print(f"Skipping {path.name} (already exists)")
            continue
        blob.upload_file_and_get_url(path.read_bytes(), blob_name, content_type="application/pdf")
        print(f"Uploaded {path.name} -> {blob_name}")
        uploaded += 1

    print(f"Uploaded {uploaded} files")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
