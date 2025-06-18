from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils import chat_completion
from app.auth.token import require_token



router = APIRouter(dependencies=[Depends(require_token)])


class QueryRequest(BaseModel):
    query: str
    session_key: str


@router.post("/ask")
def ask_question(payload: QueryRequest) -> dict[str, str]:
    """Answer a health question using recent labs and visit notes as context."""
    from app.storage.db import SessionLocal
    from app.storage import models

    session = SessionLocal()
    try:
        labs = (
            session.query(models.LabResult)
            .filter(models.LabResult.session_key == payload.session_key)
            .order_by(models.LabResult.date.desc())
            .limit(5)
            .all()
        )
        visits = (
            session.query(models.VisitSummary)
            .filter(models.VisitSummary.session_key == payload.session_key)
            .order_by(models.VisitSummary.date.desc())
            .limit(5)
            .all()
        )
        structured = (
            session.query(models.StructuredRecord)
            .filter(models.StructuredRecord.session_key == payload.session_key)
            .order_by(models.StructuredRecord.id.desc())
            .limit(5)
            .all()
        )
    finally:
        session.close()

    lab_lines = [
        f"- {lab.test_name}: {lab.value} {lab.units} ({lab.date})" for lab in labs
    ]
    visit_lines = [
        f"- {v.date} - {v.provider} - {v.doctor}: {v.notes}" for v in visits
    ]
    structured_lines = [
        f"- [{r.type}] {r.text} ({r.source_url})" if r.source_url else f"- [{r.type}] {r.text}"
        for r in structured
    ]

    context = "Recent Lab Results:\n" + "\n".join(lab_lines)
    context += "\n\nRecent Visits:\n" + "\n".join(visit_lines)
    if structured_lines:
        context += "\n\nRecent Records:\n" + "\n".join(structured_lines)

    prompt = f"{context}\n\nQuestion: {payload.query}"

    answer = chat_completion(
        [{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    return {"answer": answer}
