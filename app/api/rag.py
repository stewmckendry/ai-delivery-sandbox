from __future__ import annotations

import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils import chat_completion
from app.utils.tokens import count_tokens
from app.auth.token import require_token



logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(require_token)])


class QueryRequest(BaseModel):
    query: str
    session_key: str


class VectorQueryRequest(QueryRequest):
    top_k: int = 5


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


@router.post("/ask_vector")
def ask_question_vector(payload: VectorQueryRequest) -> dict[str, str]:
    """Answer a question using Chroma vector search if available."""
    logger.info("[/ask_vector] session=%s query=%s", payload.session_key, payload.query)
    try:
        from app.rag.searcher import search_records

        records = search_records(payload.query, payload.session_key, n_results=payload.top_k)
        logger.info("[/ask_vector] search returned %d records", len(records))
    except Exception as exc:  # noqa: BLE001
        logger.error("[/ask_vector] Vector search failed: %s", exc)
        return ask_question(QueryRequest(query=payload.query, session_key=payload.session_key))

    types = {
        r.get("clinical_type") or r.get("type")
        for r in records
        if isinstance(r, dict)
    }

    blocks: list[str] = []
    for idx, rec in enumerate(records, start=1):
        if not isinstance(rec, dict):
            continue
        lines = [f"Record {idx}:"]
        if rec.get("type"):
            lines.append(f"Type: {rec['type']}")
        if rec.get("code"):
            lines.append(f"Code: {rec['code']}")
        if rec.get("display"):
            lines.append(f"Display: {rec['display']}")
        if rec.get("portal"):
            lines.append(f"Portal: {rec['portal']}")
        text = rec.get("text", "")
        if text:
            lines.append(f"Text: {text}")
        if rec.get("source_url"):
            lines.append(f"Source: {rec['source_url']}")
        blocks.append("\n".join(lines))

    context = "\n\n".join(blocks)
    logger.info("[/ask_vector] record types: %s", ",".join(sorted(t for t in types if t)))
    prompt = f"{context}\n\nQuestion: {payload.query}" if context else payload.query
    logger.info("[/ask_vector] prompt preview: %s", prompt[:200].replace("\n", " "))
    answer = chat_completion(
        [{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
    )
    logger.info("[/ask_vector] answer preview: %s", str(answer)[:200])
    return {"answer": answer}
