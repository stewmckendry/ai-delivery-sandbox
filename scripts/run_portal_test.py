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
        run_etl_for_portal(args.portal)
        summary["success"] = True
    except Exception as exc:  # noqa: BLE001
        summary["success"] = False
        summary["error"] = str(exc)
        if args.debug:
            traceback.print_exc()

    end = datetime.utcnow()
    summary["end_time"] = end.isoformat()
    summary["duration_seconds"] = (end - start).total_seconds()

    log_dir = ROOT_DIR / "logs" / "portal_runs"
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"{args.portal}_{ts}.json"

    # Copy any challenge screenshots to the log directory
    screenshots = list(Path("/tmp").glob("challenge_*.png"))
    copied = []
    for sc in screenshots:
        if sc.stat().st_mtime < start.timestamp():
            continue
        dest = log_dir / sc.name
        try:
            shutil.copy(sc, dest)
            copied.append(dest.name)
        except Exception:
            continue
    if copied:
        summary["screenshots"] = copied

    with log_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print(f"Run complete. Log saved to {log_path}")


if __name__ == "__main__":
    main()
