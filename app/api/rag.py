from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils import chat_completion
from app.utils.tokens import count_tokens
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
            .all()
        )
        visits = (
            session.query(models.VisitSummary)
            .filter(models.VisitSummary.session_key == payload.session_key)
            .order_by(models.VisitSummary.date.desc())
            .all()
        )
        structured = (
            session.query(models.StructuredRecord)
            .filter(models.StructuredRecord.session_key == payload.session_key)
            .filter(models.StructuredRecord.is_duplicate == False)
            .order_by(models.StructuredRecord.id.desc())
            .all()
        )
    finally:
        session.close()

    token_limit = 3000 - count_tokens(f"Question: {payload.query}")
    lines: list[str] = []

    def try_add(text: str) -> bool:
        nonlocal token_limit
        tok = count_tokens(text + "\n")
        if tok > token_limit:
            return False
        lines.append(text)
        token_limit -= tok
        return True

    try_add("Recent Lab Results:")
    for lab in labs:
        if not try_add(f"- {lab.test_name}: {lab.value} {lab.units} ({lab.date})"):
            break

    try_add("")
    try_add("Recent Visits:")
    for v in visits:
        if not try_add(f"- {v.date} - {v.provider} - {v.doctor}: {v.notes}"):
            break

    seen_text: set[str] = set()
    if structured:
        try_add("")
        try_add("Recent Records:")
        for r in structured:
            if r.text in seen_text:
                continue
            seen_text.add(r.text)
            line = f"- [{r.clinical_type or r.type}] {r.text}"
            if r.source_url:
                line += f" ({r.source_url})"
            if not try_add(line):
                break

    context = "\n".join(lines)
    prompt = f"{context}\n\nQuestion: {payload.query}"

    answer = chat_completion(
        [{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    return {"answer": answer}
