import os
import json
import logging
from datetime import datetime
from app.db.database import get_db_connection

logger = logging.getLogger(__name__)

def save_artifact_and_trace(section_id, artifact_id, gate_id, text, sources, tool_outputs, user_id, project_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO artifact_section (section_id, artifact_id, gate_id, text, created_at, user_id, project_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(section_id) DO UPDATE SET
            text=excluded.text,
            created_at=excluded.created_at,
            user_id=excluded.user_id,
            project_id=excluded.project_id
    """, (section_id, artifact_id, gate_id, text, now, user_id, project_id))

    trace = json.dumps(tool_outputs)
    cursor.execute("""
        INSERT INTO reasoning_trace (section_id, trace_json, created_at, user_id, project_id)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(section_id) DO UPDATE SET
            trace_json=excluded.trace_json,
            created_at=excluded.created_at,
            user_id=excluded.user_id,
            project_id=excluded.project_id
    """, (section_id, trace, now, user_id, project_id))

    conn.commit()
    conn.close()
    return {"status": "saved"}

def log_tool_usage(tool, event, output, session_id, user_id, inputs):
    conn = get_db_connection()
    cursor = conn.cursor()

    prompt = inputs.get("prompt") or json.dumps(inputs)
    result = json.dumps(output)
    now = datetime.utcnow().isoformat()
    artifact_id = inputs.get("artifact") or inputs.get("artifact_id")
    gate_id = inputs.get("gate_id")
    project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

    cursor.execute("""
        INSERT INTO prompt_log (session_id, user_id, tool, event, prompt, result, created_at, artifact_id, gate_id, project_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (session_id, user_id, tool, event, prompt, result, now, artifact_id, gate_id, project_id))

    conn.commit()
    conn.close()

def save_document_and_trace(session_id, artifact_id, gate_id, version, storage_url, summary, inputs, output_path, tool_outputs):
    conn = get_db_connection()
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    trace = json.dumps(tool_outputs)
    project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

    cursor.execute("""
        INSERT INTO document_version_log (artifact_id, gate_id, version, storage_url, summary, created_at, path, trace_json, project_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (artifact_id, gate_id, version, storage_url, summary, now, output_path, trace, project_id))

    conn.commit()
    conn.close()