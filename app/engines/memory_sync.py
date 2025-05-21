import json
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.PromptLog import PromptLog
from app.db.models.SessionSnapshot import SessionSnapshot

LOG_DIR = "logs/prompt_logs"
SNAPSHOT_DIR = "logs/session_snapshots"
DB_URL = os.getenv("DATABASE_URL", "sqlite:///project/local/prompt_logs.db")

def log_tool_usage(tool_name, input_summary, output_summary, full_input_path, full_output_path=None, session_id=None, user_id=None):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    
    log_data = {
        "timestamp": timestamp,
        "tool": tool_name,
        "input_summary": input_summary,
        "output_summary": output_summary,
        "full_input_path": full_input_path,
        "full_output_path": full_output_path,
        "session_id": session_id,
        "user_id": user_id
    }
    with open(os.path.join(LOG_DIR, "prompt_logs.jsonl"), "a") as f:
        f.write(json.dumps(log_data) + "\n")

    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    try:
        db_log = PromptLog(
            tool=tool_name,
            input_summary=input_summary,
            output_summary=output_summary,
            full_input_path=full_input_path,
            full_output_path=full_output_path,
            session_id=session_id,
            user_id=user_id
        )
        db_session.add(db_log)
        db_session.commit()
    finally:
        db_session.close()

def save_session_snapshot(session_id, snapshot_path, notes=None, user_id=None):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    
    snapshot_data = {
        "timestamp": timestamp,
        "session_id": session_id,
        "snapshot_path": snapshot_path,
        "notes": notes,
        "user_id": user_id
    }
    with open(os.path.join(SNAPSHOT_DIR, f"snapshot_{session_id}.json"), "w") as f:
        json.dump(snapshot_data, f, indent=2)

    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    try:
        db_snapshot = SessionSnapshot(
            session_id=session_id,
            snapshot_path=snapshot_path,
            notes=notes,
            user_id=user_id
        )
        db_session.add(db_snapshot)
        db_session.commit()
    finally:
        db_session.close()

def load_latest_snapshot():
    files = sorted(os.listdir(SNAPSHOT_DIR), reverse=True)
    if not files:
        return {}
    with open(os.path.join(SNAPSHOT_DIR, files[0]), "r") as f:
        return json.load(f)