from sqlalchemy import Column, String, TIMESTAMP, JSON
from app.db.database import Base
import datetime

class ReasoningTrace(Base):
    __tablename__ = "reasoning_trace"

    trace_id = Column(String, primary_key=True)
    section_id = Column(String, nullable=False)
    steps = Column(JSON, nullable=False)
    draft_chunks = Column(JSON, nullable=True)
    created_by = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)