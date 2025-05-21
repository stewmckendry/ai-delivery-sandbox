from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SessionSnapshot(Base):
    __tablename__ = 'session_snapshots'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(255), nullable=False)
    snapshot_path = Column(String(1024))  # Where JSON snapshot is stored
    notes = Column(Text, nullable=True)  # Optional debug/context notes
    user_id = Column(String(255), nullable=True)