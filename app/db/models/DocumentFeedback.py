from sqlalchemy import Column, String, Text, TIMESTAMP
from app.db.database import Base
import datetime
import uuid

class DocumentFeedback(Base):
    __tablename__ = "document_feedback"

    document_feedback_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, nullable=False)
    submitted_by = Column(String, nullable=True)
    feedback_text = Column(Text, nullable=False)
    feedback_type = Column(String, default="general")
    status = Column(String, default="open")
    linked_task_id = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    resolved_at = Column(TIMESTAMP, nullable=True)
    project_id = Column(String, nullable=True)