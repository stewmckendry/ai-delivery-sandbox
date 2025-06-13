#!/usr/bin/env python
"""Export structured DB records to JSON, Markdown, or PDF."""
from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple
import logging

import markdown2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Ensure repo root is on path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)




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


def _fetch_records(session, models_module) -> Tuple[List, List, List]:
    labs = (
        session.query(models_module.LabResult)
        .order_by(models_module.LabResult.date)
        .all()
    )
    visits = (
        session.query(models_module.VisitSummary)
        .order_by(models_module.VisitSummary.date)
        .all()
    )
    try:
        structured = (
            session.query(models_module.StructuredRecord)
            .order_by(models_module.StructuredRecord.id)
            .all()
        )
    except Exception:  # pragma: no cover - older DBs may lack table
        structured = []
    logger.info(
        "Fetched %d labs, %d visits, %d structured records",
        len(labs),
        len(visits),
        len(structured),
    )
    return labs, visits, structured


def _records_to_markdown(labs, visits, structured) -> str:
    lines = []
    if labs:
        lines.append("## Lab Results")
        for lab in labs:
            lines.append(
                f"- {lab.date} {lab.test_name} {lab.value} {lab.units}")
        lines.append("")
    if visits:
        lines.append("## Visit Summaries")
        for visit in visits:
            lines.append(
                f"- {visit.date} {visit.provider} {visit.doctor}: {visit.notes}")
        lines.append("")
    if structured:
        lines.append("## Structured Records")
        for rec in structured:
            base = f"- [{rec.type}] {rec.text}"
            if rec.source_url:
                base += f" ({rec.source_url})"
            lines.append(base)
    return "\n".join(lines)


def _markdown_to_pdf(md: str, out_path: Path) -> None:
    """Render ``md`` to a simple PDF using reportlab."""
    pdf = canvas.Canvas(str(out_path), pagesize=letter)
    text = pdf.beginText(40, 750)
    for line in md.splitlines():
        text.textLine(line)
        if text.getY() <= 40:
            pdf.drawText(text)
            pdf.showPage()
            text = pdf.beginText(40, 750)
    pdf.drawText(text)
    pdf.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export structured DB records")
    parser.add_argument("--db", default="health_data.db", help="SQLite DB path")
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "pdf"],
        default="json",
        help="Output format",
    )
    parser.add_argument("--output", required=True, help="Output file path")
    args = parser.parse_args()

    session, models_module = _init_session(args.db)
    labs, visits, structured = _fetch_records(session, models_module)
    session.close()

    out_path = Path(args.output)

    if args.format == "json":
        data = {
            "lab_results": [
                {
                    "test_name": l.test_name,
                    "value": l.value,
                    "units": l.units,
                    "date": l.date.isoformat(),
                }
                for l in labs
            ],
            "visit_summaries": [
                {
                    "provider": v.provider,
                    "doctor": v.doctor,
                    "notes": v.notes,
                    "date": v.date.isoformat(),
                }
                for v in visits
            ],
            "structured_records": [
                {
                    "portal": r.portal,
                    "type": r.type,
                    "text": r.text,
                    "source_url": r.source_url,
                    "date_created": r.date_created.isoformat(),
                }
                for r in structured
            ],
        }
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    else:
        md = _records_to_markdown(labs, visits, structured)
        if args.format == "markdown":
            out_path.write_text(md, encoding="utf-8")
        else:  # pdf
            _markdown_to_pdf(md, out_path)

    logger.info("Exported records to %s", out_path)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
