import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Text
from app.db.database import Base

class PromptLog(Base):
    __tablename__ = 'prompt_logs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tool = Column(String(255))
    input_summary = Column(Text)
    output_summary = Column(Text)
    full_input_path = Column(Text)  # Store full input metadata or JSON blob
    full_output_path = Column(Text)  # Store full output result or JSON blob
    session_id = Column(String(255))
    user_id = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tool": self.tool,
            "input_summary": self.input_summary,
            "output_summary": self.output_summary,
            "full_input_path": self.full_input_path,
            "full_output_path": self.full_output_path,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }