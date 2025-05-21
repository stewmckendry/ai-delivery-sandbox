from sqlalchemy import Column, DateTime, String
from app.db.database import Base

class SessionSnapshot(Base):
    __tablename__ = 'session_snapshots'

    snapshot_id = Column(String(255), primary_key=True)
    session_id = Column(String(255))
    path = Column(String(1024))
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            'snapshot_id': self.snapshot_id,
            'session_id': self.session_id,
            'path': self.path,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }