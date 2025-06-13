from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.utils import chat_completion



router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/ask")
def ask_question(payload: QueryRequest) -> dict[str, str]:
    """Answer a health question using recent labs and visit notes as context."""
    from app.storage.db import SessionLocal
    from app.storage import models

    session = SessionLocal()
    try:
        labs = (
            session.query(models.LabResult)
            .order_by(models.LabResult.date.desc())
            .limit(5)
            .all()
        )
        visits = (
            session.query(models.VisitSummary)
            .order_by(models.VisitSummary.date.desc())
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

    context = "Recent Lab Results:\n" + "\n".join(lab_lines)
    context += "\n\nRecent Visits:\n" + "\n".join(visit_lines)

    prompt = f"{context}\n\nQuestion: {payload.query}"

    answer = chat_completion(
        [{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    return {"answer": answer}
