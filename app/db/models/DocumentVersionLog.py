from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class DocumentVersionLog(Base):
    __tablename__ = "document_version_log"

    doc_version_id = Column(String(255), primary_key=True)
    artifact_name = Column(String(255), nullable=False)
    gate = Column(Integer, nullable=False)
    version_tag = Column(String(255), nullable=False)
    submitted_by = Column(String(255), nullable=True)
    file_path = Column(String(255), nullable=False)
    google_doc_url = Column(String(255), nullable=True)
    doc_format = Column(String(50), default="markdown")
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)