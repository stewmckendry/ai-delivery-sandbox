import datetime
import os
import json
from app.db.models import PromptLog
from app.db.database import get_db

def log_tool_usage(tool_name, input_summary, output_summary, session_id, user_id=None, metadata=None):
    db = get_db()

    prompt_log = PromptLog(
        tool=tool_name,
        input_summary=input_summary,
        output_summary=output_summary,
        full_input_path=None,
        full_output_path=None,
        session_id=session_id,
        user_id=user_id,
        timestamp=datetime.datetime.utcnow(),
        metadata=metadata if metadata else {}
    )

    db.add(prompt_log)
    db.commit()
    db.refresh(prompt_log)

    return prompt_log.id