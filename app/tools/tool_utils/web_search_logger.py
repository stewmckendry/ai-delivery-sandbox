from datetime import datetime
from app.db.models.WebSearchLog import WebSearchLog
from sqlalchemy.orm import Session

def log_web_search(db: Session, **kwargs):
    log_entry = WebSearchLog(
        search_type=kwargs.get("search_type"),
        query=kwargs.get("query"),
        results_summary=kwargs.get("results_summary"),
        tool_invoked_by=kwargs.get("tool_invoked_by"),
        user_id=kwargs.get("user_id"),
        session_id=kwargs.get("session_id"),
        project_id=kwargs.get("project_id"),  # now explicitly a string
        timestamp=datetime.utcnow()
    )
    db.add(log_entry)
    db.commit()