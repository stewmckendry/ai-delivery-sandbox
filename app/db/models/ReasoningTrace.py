from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mssql import NVARCHAR
from app.db.database import Base
import datetime

class ReasoningTrace(Base):
    __tablename__ = "reasoning_trace"

    trace_id = Column(String(255), primary_key=True)
    section_id = Column(String(255), nullable=False)
    steps = Column(NVARCHAR(None), nullable=False)  # ordered list of reasoning steps as JSON string
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    draft_chunks = Column(NVARCHAR(None), nullable=True)  # optional: store each draft section separately as JSON string