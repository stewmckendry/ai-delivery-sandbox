from sqlalchemy import Column, String, Text, TIMESTAMP
from app.db.database import Base
import datetime
import uuid

class ArtifactSection(Base):
    __tablename__ = "artifact_section"

    artifact_section_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    section_id = Column(String, index=True)
    artifact_id = Column(String, nullable=False)
    gate_id = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    sources = Column(Text)  # Optional JSON string of citations/sources
    status = Column(String, default="draft")
    generated_by = Column(String, nullable=True)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    version = Column(String, default="v1")