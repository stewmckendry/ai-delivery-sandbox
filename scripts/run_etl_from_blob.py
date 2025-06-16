#!/usr/bin/env python
"""Run ETL pipeline on uploaded Azure Blob files."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.orchestrator import run_etl_from_blobs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ETL for blob uploads")
    parser.add_argument("--prefix", required=True, help="Blob prefix e.g. user/session")
    args = parser.parse_args()

    start = datetime.utcnow()
    try:
        run_etl_from_blobs(args.prefix)
        success = True
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}")
        success = False
    end = datetime.utcnow()
    print(f"Finished in {(end - start).total_seconds():.1f}s - success={success}")


if __name__ == "__main__":
    main()
