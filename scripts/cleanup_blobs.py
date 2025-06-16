#!/usr/bin/env python
"""Delete expired Azure blob uploads."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.storage import blob


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove old blobs")
    parser.add_argument(
        "--prefix", default="", help="Prefix path to filter e.g. user/session"
    )
    parser.add_argument(
        "--ttl-hours",
        type=float,
        default=24.0,
        help="Delete blobs older than this many hours",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="List blobs without deleting"
    )
    args = parser.parse_args()

    info = blob.list_blob_info(args.prefix)
    expired = [b for b in info if b["age_hours"] >= args.ttl_hours]

    print(f"{len(expired)} expired blobs found (ttl={args.ttl_hours}h)")
    for item in expired:
        age = item["age_hours"]
        print(f"- {item['name']} {age:.1f}h")

    if not args.dry_run:
        for item in expired:
            blob.delete_blob(item["name"])
        print(f"Deleted {len(expired)} blobs")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
