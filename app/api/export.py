from __future__ import annotations

from tempfile import NamedTemporaryFile
from pathlib import Path

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse

from app.storage.db import SessionLocal, init_db
from app.storage import models
from app.auth.token import require_token

router = APIRouter(dependencies=[Depends(require_token)])


def _records_to_markdown(labs, visits, structured) -> str:
    lines = []
    if labs:
        lines.append("## Lab Results")
        for lab in labs:
            lines.append(f"- {lab.date.isoformat()} {lab.test_name} {lab.value} {lab.units}")
        lines.append("")
    if visits:
        lines.append("## Visit Summaries")
        for visit in visits:
            lines.append(f"- {visit.date.isoformat()} {visit.provider} {visit.doctor}: {visit.notes}")
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
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

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


@router.get("/export")
def export_records(
    session_key: str = Query(...),
    format: str = Query("json", enum=["json", "markdown", "pdf"]),
):
    """Export structured records for ``session_key`` in the given ``format``."""
    init_db()
    session = SessionLocal()
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
    finally:
        session.close()

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
        return JSONResponse(data)

    md = _records_to_markdown(labs, visits, structured)
    if format == "markdown":
        return PlainTextResponse(md, media_type="text/markdown")

    tmp = NamedTemporaryFile(delete=False, suffix=".pdf")
    path = Path(tmp.name)
    _markdown_to_pdf(md, path)
    return FileResponse(path, media_type="application/pdf", filename="records.pdf")
