import os
import yaml
import datetime
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.db.models.PromptLog import PromptLog
from app.db.models.SessionSnapshot import SessionSnapshot
from app.engines.memory_sync import SNAPSHOT_DIR

class Tool:
    def validate(self, input_dict):
        # Accepts optional session_id
        pass

    def run_tool(self, input_dict):
        session_id = input_dict.get("session_id")

        db_url = os.getenv("DATABASE_URL", "sqlite:///policy_gpt.db")
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        db = Session()

        query = db.query(PromptLog)
        if session_id:
            query = query.filter(PromptLog.session_id == session_id)
        entries = query.all()

        if not entries:
            return {"status": "no entries found"}

        entries_dicts = [e.to_dict() for e in entries]

        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        snapshot_id = str(uuid.uuid4())
        snapshot_path = os.path.join(SNAPSHOT_DIR, f"snapshot_{session_id or 'global'}_{timestamp}.yaml")

        with open(snapshot_path, "w") as f:
            yaml.dump(entries_dicts, f, sort_keys=False)

        snapshot_record = SessionSnapshot(
            snapshot_id=snapshot_id,
            session_id=session_id,
            path=snapshot_path,
            created_at=datetime.datetime.utcnow()
        )
        db.add(snapshot_record)
        db.commit()

        return {"status": "success", "path": snapshot_path, "entries": len(entries_dicts)}