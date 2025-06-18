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
logger.propagate = False

from app.utils import llm

from dotenv import load_dotenv
load_dotenv()

def _init_session(db_path: str):
    """Initialize DB session for ``db_path`` and return (session, models)."""
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        db_url = f"sqlite:///{db_path}"
        os.environ["DATABASE_URL"] = db_url
        logger.info("Using DATABASE_URL from argument")
    else:
        logger.info("Using DATABASE_URL from environment")
    """
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    return db_module.SessionLocal(), models_module


def _fetch_recent_records(session, models_module, session_key: str | None = None):
    """Return recent lab, visit and structured records."""
    labs = (
        session.query(models_module.LabResult)
        .order_by(models_module.LabResult.date.desc())
        .all()
    )
    visits = (
        session.query(models_module.VisitSummary)
        .order_by(models_module.VisitSummary.date.desc())
        .all()
    )
    try:
        query = session.query(models_module.StructuredRecord)
        if session_key is not None:
            query = query.filter(models_module.StructuredRecord.session_key == session_key)
        structured = (
            query.filter(models_module.StructuredRecord.is_duplicate == False)
            .order_by(models_module.StructuredRecord.id.desc())
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


def _records_to_context(labs, visits, structured, *, token_limit: int = 3000) -> str:
    """Format DB records as bullet list context, bounded by ``token_limit``."""
    from app.utils.tokens import count_tokens

    remaining = token_limit
    lines: list[str] = []

    def try_add(text: str) -> bool:
        nonlocal remaining
        tok = count_tokens(text + "\n")
        if tok > remaining:
            return False
        lines.append(text)
        remaining -= tok
        return True

    try_add("Recent Lab Results:")
    for lab in labs:
        if not try_add(f"- {lab.test_name}: {lab.value} {lab.units} ({lab.date})"):
            break

    try_add("")
    try_add("Recent Visits:")
    for v in visits:
        if not try_add(f"- Visit {v.date} with {v.doctor} at {v.provider}: {v.notes}"):
            break

    seen_text: set[str] = set()
    if structured:
        try_add("")
        try_add("Recent Records:")
        for r in structured:
            if r.text in seen_text:
                continue
            seen_text.add(r.text)
            src = f" ({r.source_url})" if r.source_url else ""
            line = f"- [{r.clinical_type or r.type}] {r.text}{src}"
            if not try_add(line):
                break

    return "\n".join(lines)


def ask(db: str, query: str, session_key: str | None = None) -> tuple[str, dict]:
    """Return answer and record counts for ``query`` using ``db``."""
    session, models_module = _init_session(db)
    labs, visits, structured = _fetch_recent_records(session, models_module, session_key)
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
    return answer, meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask questions about stored records")
    parser.add_argument("--query", required=True, help="User question")
    parser.add_argument("--db", default="health_data.db", help="SQLite DB path")
    parser.add_argument("--session", default=None, help="Session key to filter records")
    args = parser.parse_args()

    answer, meta = ask(args.db, args.query, session_key=args.session)
    logger.info(answer)
    logger.info(
        "Context size: %d labs, %d visits, %d structured records",
        meta["labs"],
        meta["visits"],
        meta["structured_records"],
    )


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
