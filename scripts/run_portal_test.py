#!/usr/bin/env python
"""Command line tool to execute the ETL pipeline for a single portal.

This script is intended for manual testing of the full pipeline. It calls
``run_etl_for_portal`` from ``app.orchestrator`` and records a summary
of the run to ``logs/portal_runs/<portal>_<timestamp>.json``.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
import shutil
from dotenv import load_dotenv
load_dotenv()

# Ensure ``app`` package imports resolve when run directly
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))



def main() -> None:
    parser = argparse.ArgumentParser(description="Run ETL pipeline for a portal")
    parser.add_argument("--portal", required=True, help="Portal name (module)")
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Max crawl depth/pages (stored in MAX_DEPTH env)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print stack traces if the pipeline fails",
    )
    args = parser.parse_args()

    # Use an in-memory Redis instance for test runs unless disabled
    if os.getenv("USE_FAKE_REDIS", "1") == "1":
        import importlib
        import fakeredis

        import app.storage.redis as redis_module

        redis_module = importlib.reload(redis_module)
        redis_module._redis_client = fakeredis.FakeRedis(decode_responses=True)

    # Import here so pytest collection doesn't require environment variables
    from app.orchestrator import run_etl_for_portal

    os.environ["MAX_DEPTH"] = str(args.depth)

    start = datetime.utcnow()
    summary = {
        "portal": args.portal,
        "depth": args.depth,
        "start_time": start.isoformat(),
    }

    try:
        etl_summary = run_etl_for_portal(args.portal)
        summary["success"] = True
    except Exception as exc:  # noqa: BLE001
        summary["success"] = False
        summary["error"] = str(exc)
        if args.debug:
            traceback.print_exc()

    end = datetime.utcnow()
    summary["end_time"] = end.isoformat()
    summary["duration_seconds"] = (end - start).total_seconds()

    print("Run complete. Summary:\n")
    print(json.dumps(summary, indent=2))
    if summary.get("success"):
        print(etl_summary)


if __name__ == "__main__":
    main()
