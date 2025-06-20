#!/usr/bin/env python
"""Delete Azure blobs by name or remove all blobs from the container.

Examples:
    Delete a single blob::
        python scripts/delete_blobs.py --name session_key/filename.pdf

    Delete multiple blobs::
        python scripts/delete_blobs.py --name sess1/file1.txt --name sess2/file2.txt

    Delete all blobs in the container::
        python scripts/delete_blobs.py --all

Blob names use the ``session_key/filename`` format.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Ensure repo root is on sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.storage import blob


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete blobs from Azure storage")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--name",
        action="append",
        dest="names",
        help="Blob name in session_key/filename format. May be repeated.",
    )
    group.add_argument(
        "--all",
        action="store_true",
        help="Delete every blob in the container",
    )
    args = parser.parse_args()

    if args.all:
        names = blob.list_blobs("")
    else:
        names = args.names or []

    if not names:
        print("No blobs to delete")
        return

    for name in names:
        blob.delete_blob(name)
    print(f"Deleted {len(names)} blobs")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
