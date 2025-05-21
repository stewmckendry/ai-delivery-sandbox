import uuid
import datetime
from sqlalchemy import Column, String, DateTime
from app.db.database import Base

class PromptLog(Base):
    __tablename__ = 'prompt_logs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(255))
    source = Column(String(255))
    type = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    content_summary = Column(String)
    tags = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "source": self.source,
            "type": self.type,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "content_summary": self.content_summary,
            "tags": self.tags
        }