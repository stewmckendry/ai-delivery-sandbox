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

from dotenv import load_dotenv
load_dotenv()

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
        db_url = f"sqlite:///{db_path}"
        os.environ["DATABASE_URL"] = db_url
        logger.info("Using DATABASE_URL from argument")
    else:
        logger.info("Using DATABASE_URL from environment")
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()
    return db_module.SessionLocal(), models_module


def _fetch_records(session, models_module, session_key: str | None = None) -> Tuple[List, List, List]:
    labs_q = session.query(models_module.LabResult).order_by(models_module.LabResult.date)
    visits_q = session.query(models_module.VisitSummary).order_by(models_module.VisitSummary.date)
    if session_key is not None:
        labs_q = labs_q.filter(models_module.LabResult.session_key == session_key)
        visits_q = visits_q.filter(models_module.VisitSummary.session_key == session_key)
    labs = labs_q.all()
    visits = visits_q.all()
    try:
        query = session.query(models_module.StructuredRecord)
        if session_key is not None:
            query = query.filter(models_module.StructuredRecord.session_key == session_key)
        structured = query.order_by(models_module.StructuredRecord.id).all()
    except Exception:  # pragma: no cover - older DBs may lack table
        structured = []
    logger.info(
        "Fetched %d labs, %d visits, %d structured records",
        len(labs),
        len(visits),
        len(structured),
    )
    return labs, visits, structured


def _fetch_fhir_resources(session, models_module, labs, visits):
    rows: list = []
    lab_ids = [l.id for l in labs]
    visit_ids = [v.id for v in visits]
    if lab_ids:
        rows.extend(
            session.query(models_module.FHIRResource)
            .filter(
                models_module.FHIRResource.record_type == "lab",
                models_module.FHIRResource.record_id.in_(lab_ids),
            )
            .all()
        )
    if visit_ids:
        rows.extend(
            session.query(models_module.FHIRResource)
            .filter(
                models_module.FHIRResource.record_type == "visit",
                models_module.FHIRResource.record_id.in_(visit_ids),
            )
            .all()
        )
    logger.info("Fetched %d FHIR resources", len(rows))
    return rows


def _records_to_markdown(labs, visits, structured) -> str:
    """Convert DB records to a human-readable Markdown summary."""
    lines: list[str] = []
    if labs:
        lines.append("## Lab Results")
        for lab in labs:
            lines.append(f"- {lab.date}: {lab.test_name} {lab.value} {lab.units}")
        lines.append("")
    if visits:
        lines.append("## Visit Notes")
        for visit in visits:
            lines.append(f"- {visit.date}: {visit.provider} {visit.doctor} \u2014 {visit.notes}")
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
    """Render ``md`` to a simple, human-friendly PDF."""
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=11,
            leading=14,
        )
    )
    styles["Heading2"].fontName = "Helvetica-Bold"
    styles["Heading2"].fontSize = 14

    doc = SimpleDocTemplate(str(out_path), pagesize=letter, topMargin=0.75 * inch)
    elements = []
    for line in md.splitlines():
        if line.startswith("## "):
            elements.append(Paragraph(line[3:], styles["Heading2"]))
            elements.append(Spacer(1, 0.2 * inch))
        elif line.startswith("- "):
            elements.append(Paragraph(line[2:], styles["Body"]))
        elif not line.strip():
            elements.append(Spacer(1, 0.2 * inch))
        else:
            elements.append(Paragraph(line, styles["Body"]))
    doc.build(elements)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export structured DB records")
    parser.add_argument("--db", default="health_data.db", help="SQLite DB path")
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "pdf", "fhir"],
        default="json",
        help="Output format",
    )
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--session", default=None, help="Session key to filter records")
    args = parser.parse_args()

    session, models_module = _init_session(args.db)
    labs, visits, structured = _fetch_records(session, models_module, args.session)
    fhir_rows = []
    if args.format == "fhir":
        fhir_rows = _fetch_fhir_resources(session, models_module, labs, visits)
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
    elif args.format == "fhir":
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {"resource": json.loads(r.resource_json)} for r in fhir_rows
            ],
        }
        out_path.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    else:
        md = _records_to_markdown(labs, visits, structured)
        if args.format == "markdown":
            out_path.write_text(md, encoding="utf-8")
        else:  # pdf
            _markdown_to_pdf(md, out_path)

    logger.info("Exported records to %s", out_path)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
