from typing import List, Dict

from sqlalchemy.orm import Session

from app.storage import models

from app.utils import chat_completion


def summarize_blocks(blocks: List[Dict[str, str]]) -> str:
    """Return a natural-language summary of text blocks using OpenAI.

    Parameters
    ----------
    blocks: List[Dict[str, str]]
        Sequence of dictionaries each containing a ``"text"`` field.

    Returns
    -------
    str
        Concise summary of the provided text.
    """

    system_prompt = (
        "Summarize the following content in a way that highlights key details "
        "clearly. Assume the text may include medical records, summaries, or "
        "observations. Output a concise, readable summary."
    )

    combined_text = "\n".join(block.get("text", "") for block in blocks)
    return chat_completion(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_text},
        ],
        model="gpt-3.5-turbo",
    )


def summarize_database_records(session: Session) -> str:
    """Generate a markdown summary of all structured DB records."""

    visits = session.query(models.VisitSummary).order_by(models.VisitSummary.date).all()
    labs = session.query(models.LabResult).order_by(models.LabResult.date).all()
    structured = session.query(models.StructuredRecord).order_by(models.StructuredRecord.id).all()

    blocks: List[Dict[str, str]] = []
    for v in visits:
        blocks.append({"text": f"Visit on {v.date} with {v.doctor} at {v.provider}. {v.notes}"})
    for l in labs:
        blocks.append({"text": f"{l.test_name} {l.value} {l.units} on {l.date}"})
    for r in structured:
        blocks.append({"text": r.text})

    summary_body = summarize_blocks(blocks) if blocks else "No records found." 

    header = (
        f"### Portal Run Summary\n\n"
        f"The patient had {len(visits)} visits and {len(labs)} lab results."
    )

    return f"{header}\n\n{summary_body}"
