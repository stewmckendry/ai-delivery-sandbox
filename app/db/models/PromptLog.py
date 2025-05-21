from sqlalchemy import Column, String, DateTime, Text
from app.db.database import Base
import datetime

class PromptLog(Base):
    __tablename__ = "prompt_logs"

    id = Column(String, primary_key=True)
    session_id = Column(String)
    source = Column(String)
    type = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    content_summary = Column(Text)
    tags = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "source": self.source,
            "type": self.type,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "content_summary": self.content_summary,
            "tags": self.tags,
        }