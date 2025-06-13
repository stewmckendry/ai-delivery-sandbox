from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime

from .db import Base, engine


class LabResult(Base):
    """Model for a single lab test result."""

    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True)
    test_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    units = Column(String, nullable=False)
    date = Column(Date, nullable=False)


class VisitSummary(Base):
    """Model for a visit summary note."""

    __tablename__ = "visit_summaries"

    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    doctor = Column(String, nullable=False)
    notes = Column(String, nullable=False)
    date = Column(Date, nullable=False)


class StructuredRecord(Base):
    """Model for cleaned AI-extracted record."""

    __tablename__ = "structured_records"

    id = Column(Integer, primary_key=True, index=True)
    portal = Column(String)
    type = Column(String)
    text = Column(Text)
    source_url = Column(String)
    date_created = Column(DateTime, default=datetime.utcnow)


# Ensure tables are created when imported
Base.metadata.create_all(bind=engine)
