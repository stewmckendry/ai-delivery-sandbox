import os
import json
import logging
import datetime
from decimal import Decimal
from app.db.connect import Session
from app.db.models.MemoryLog import MemoryLog

logger = logging.getLogger(__name__)

def safe_json(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def log_tool_usage(tool_name, input_summary, output_summary, session_id, user_id, metadata=None):
    try:
        session = Session()
        full_input = json.dumps(metadata, indent=2, default=safe_json) if metadata else None
        log = MemoryLog(
            tool=tool_name,
            input_summary=input_summary,
            output_summary=output_summary,
            session_id=session_id,
            user_id=user_id,
            full_input=full_input
        )
        session.add(log)
        session.commit()
        logger.info(f"Logged tool usage: {tool_name} by user {user_id}")
    except Exception as e:
        logger.warning(f"Failed to log tool usage: {e}")
    finally:
        session.close()