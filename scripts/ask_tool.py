#!/usr/bin/env python
"""Query structured health records via the command line."""
from __future__ import annotations

import argparse
import importlib
import os
import sys
from pathlib import Path
import logging

# Ensure repo root on path so `app` imports resolve when executed directly
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

from app.utils import llm


def _init_session(db_path: str):
    """Initialize DB session for ``db_path`` and return (session, models)."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_file = Path(db_path).resolve()
        db_url = f"sqlite:///{db_file}"
        os.environ["DATABASE_URL"] = db_url
        logger.info("Using DATABASE_URL from argument: %s", db_url)
    else:
        logger.info("Using DATABASE_URL from environment: %s", db_url)
        if db_url.startswith("sqlite:///"):
            db_file = Path(db_url.replace("sqlite:///", "")).resolve()
            db_url = f"sqlite:///{db_file}"
            os.environ["DATABASE_URL"] = db_url
    logger.info("Resolved DB file path: %s", db_url.replace("sqlite:///", ""))
    db_file = Path(db_url.replace("sqlite:///", ""))
    logger.info("DB file exists: %s", db_file.exists())
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    return db_module.SessionLocal(), models_module


def _fetch_recent_records(session, models_module):
    """Return recent lab, visit and structured records."""
    labs = (
        session.query(models_module.LabResult)
        .order_by(models_module.LabResult.date.desc())
        .limit(5)
        .all()
    )
    visits = (
        session.query(models_module.VisitSummary)
        .order_by(models_module.VisitSummary.date.desc())
        .limit(5)
        .all()
    )
    try:
        structured = (
            session.query(models_module.StructuredRecord)
            .order_by(models_module.StructuredRecord.id.desc())
            .limit(5)
            .all()
        )
    except Exception:  # pragma: no cover - table may be missing
        structured = []
    logger.info(
        "Fetched %d labs, %d visits, %d structured records",
        len(labs),
        len(visits),
        len(structured),
    )
    return labs, visits, structured


def _records_to_context(labs, visits, structured) -> str:
    """Format DB records as bullet list context."""
    lines = []
    for lab in labs:
        lines.append(f"- {lab.test_name}: {lab.value} {lab.units} ({lab.date})")
    for v in visits:
        lines.append(
            f"- Visit {v.date} with {v.doctor} at {v.provider}: {v.notes}"
        )
    for r in structured:
        src = f" ({r.source_url})" if r.source_url else ""
        lines.append(f"- [{r.type}] {r.text}{src}")
    return "\n".join(lines)


def ask(db: str, query: str) -> tuple[str, dict]:
    """Return answer and record counts for ``query`` using ``db``."""
    session, models_module = _init_session(db)
    labs, visits, structured = _fetch_recent_records(session, models_module)
    session.close()

    logger.info("Running query: %s", query)

    context = _records_to_context(labs, visits, structured)
    prompt = f"{context}\n\nQuestion: {query}"
    answer = llm.chat_completion(
        [{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    logger.info("LLM answered")
    meta = {
        "labs": len(labs),
        "visits": len(visits),
        "structured_records": len(structured),
    }
    logger.info(
        "Context size: %d labs, %d visits, %d structured records",
        meta["labs"],
        meta["visits"],
        meta["structured_records"],
    )
    return answer, meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions about stored records")
    parser.add_argument("--query", required=True, help="User question")
    parser.add_argument("--db", default="health_data.db", help="SQLite DB path")
    args = parser.parse_args()

    answer, meta = ask(args.db, args.query)
    logger.info(answer)
    logger.info(
        "Context size: %d labs, %d visits, %d structured records",
        meta["labs"],
        meta["visits"],
        meta["structured_records"],
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
