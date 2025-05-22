import datetime
import os
import json
from sqlalchemy.orm import Session
from app.db.models.PromptLog import PromptLog
from app.db.database import get_session

def log_tool_usage(tool_name, input_summary, output_summary, session_id, user_id=None, metadata=None):
    db: Session = get_session()

    full_input = json.dumps(metadata, indent=2) if metadata else None
    full_output = json.dumps(output_summary, indent=2) if isinstance(output_summary, (dict, list)) else output_summary

    prompt_log = PromptLog(
        tool=tool_name,
        input_summary=input_summary,
        output_summary=output_summary,
        full_input_path=full_input,
        full_output_path=full_output,
        session_id=session_id,
        user_id=user_id,
        timestamp=datetime.datetime.utcnow(),
    )

    db.add(prompt_log)
    db.commit()
    db.refresh(prompt_log)

    return prompt_log.id