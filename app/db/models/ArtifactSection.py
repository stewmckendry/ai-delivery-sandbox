from sqlalchemy import Column, String, Text, TIMESTAMP
from app.db.database import Base
import datetime

class ArtifactSection(Base):
    __tablename__ = "artifact_section"

    section_id = Column(String, primary_key=True)
    artifact_id = Column(String, nullable=False)
    gate_id = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    sources = Column(Text)  # Optional JSON string of citations/sources
    status = Column(String, default="draft")
    generated_by = Column(String, nullable=True)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)