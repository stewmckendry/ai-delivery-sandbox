from sqlalchemy import Column, String, DateTime
from app.db.database import Base
import datetime

class SessionSnapshot(Base):
    __tablename__ = "session_snapshots"

    snapshot_id = Column(String, primary_key=True)
    session_id = Column(String)
    path = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "snapshot_id": self.snapshot_id,
            "session_id": self.session_id,
            "path": self.path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }