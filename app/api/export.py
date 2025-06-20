from __future__ import annotations

from tempfile import NamedTemporaryFile
from pathlib import Path
from datetime import datetime

import json

import logging
from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse

from app.storage.db import SessionLocal, init_db
from app.storage import models, blob
from app.auth.token import require_token

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(require_token)])


def _records_to_markdown(labs, visits, structured) -> str:
    """Convert DB records to a human-readable Markdown summary."""
    lines: list[str] = []
    if labs:
        lines.append("## Lab Results")
        for lab in labs:
            lines.append(
                f"- {lab.date.isoformat()}: {lab.test_name} {lab.value} {lab.units}"
            )
        lines.append("")
    if visits:
        lines.append("## Visit Notes")
        for visit in visits:
            lines.append(
                f"- {visit.date.isoformat()}: {visit.provider} {visit.doctor} \u2014 {visit.notes}"
            )
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
    from reportlab.lib.pagesizes import letter
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


@router.get("/export")
def export_records(
    session_key: str = Query(...),
    format: str = Query("json", enum=["json", "markdown", "pdf", "fhir"]),
):
    """Export structured records for ``session_key`` in the given ``format``."""
    logger.info("[/export] session=%s format=%s", session_key, format)
    init_db()
    session = SessionLocal()
    fhir_rows: list[models.FHIRResource] = []
    try:
        labs = (
            session.query(models.LabResult)
            .filter(models.LabResult.session_key == session_key)
            .order_by(models.LabResult.date)
            .all()
        )
        visits = (
            session.query(models.VisitSummary)
            .filter(models.VisitSummary.session_key == session_key)
            .order_by(models.VisitSummary.date)
            .all()
        )
        structured = (
            session.query(models.StructuredRecord)
            .filter(models.StructuredRecord.session_key == session_key)
            .order_by(models.StructuredRecord.id)
            .all()
        )
        fhir_rows: list[models.FHIRResource] = []
        if format == "fhir":
            lab_ids = [l.id for l in labs]
            visit_ids = [v.id for v in visits]
            if lab_ids:
                fhir_rows.extend(
                    session.query(models.FHIRResource)
                    .filter(
                        models.FHIRResource.record_type == "lab",
                        models.FHIRResource.record_id.in_(lab_ids),
                    )
                    .all()
                )
            if visit_ids:
                fhir_rows.extend(
                    session.query(models.FHIRResource)
                    .filter(
                        models.FHIRResource.record_type == "visit",
                        models.FHIRResource.record_id.in_(visit_ids),
                    )
                    .all()
                )
    finally:
        session.close()
    logger.info(
        "[/export] found labs=%d visits=%d structured=%d",
        len(labs),
        len(visits),
        len(structured),
    )

    blob_data: bytes | str
    ext: str

    if format == "json":
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
        blob_data = json.dumps(data, indent=2)
        ext = "json"
    elif format == "fhir":
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {"resource": json.loads(row.resource_json)} for row in fhir_rows
            ],
        }
        blob_data = json.dumps(bundle, indent=2)
        ext = "json"
    elif format == "markdown":
        blob_data = _records_to_markdown(labs, visits, structured)
        ext = "md"
    else:
        md = _records_to_markdown(labs, visits, structured)
        tmp = NamedTemporaryFile(delete=False, suffix=".pdf")
        path = Path(tmp.name)
        _markdown_to_pdf(md, path)
        blob_data = path.read_bytes()
        path.unlink(missing_ok=True)
        ext = "pdf"

    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    if ext == "pdf":
        blob_name = f"exports/health_summary_{session_key[:5]}_{ts}.pdf"
    else:
        blob_name = f"exports/{session_key}_{ts}.{ext}"
    url = blob.upload_file_and_get_url(blob_data, blob_name)
    total_recs = len(labs) + len(visits) + len(structured)
    if total_recs == 0:
        logger.error("[/export] no records exported for session %s", session_key)
    logger.info("[/export] exported %d records to %s", total_recs, blob_name)
    return JSONResponse({"status": "ok", "download_url": url})
