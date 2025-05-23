from app.db.models.PromptLog import PromptLog
from app.db.database import db_session
from datetime import datetime

def memory_retrieve(context):
    """
    Retrieves relevant PromptLog entries that contain user inputs,
    based on artifact_id and section_id passed in context.
    """
    artifact = context.get("artifact")
    section = context.get("section")
    if not artifact or not section:
        raise ValueError("artifact and section must be provided in context")

    # Query PromptLog and filter by input tools (heuristic by name)
    entries = db_session.query(PromptLog).filter(
        PromptLog.tool.in_(["uploadTextInput", "loadCorpus"]),
        PromptLog.full_input_path.like(f'%"artifact": "{artifact}"%'),
        PromptLog.full_input_path.like(f'%"section": "{section}"%')
    ).order_by(PromptLog.timestamp.asc()).all()

    return [{
        "input_summary": e.input_summary,
        "output_summary": e.output_summary,
        "full_input_path": e.full_input_path,
        "timestamp": e.timestamp.isoformat()
    } for e in entries]