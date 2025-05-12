from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SymptomLog(Base):
    __tablename__ = "symptom_log_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    timestamp = Column(DateTime)
    symptoms = Column(Text)
    metadata = Column(Text)

class TrackerMetadata(Base):
    __tablename__ = "tracker_export"

    user_id = Column(String, primary_key=True)
    injury_date = Column(DateTime)
    last_checkin_time = Column(DateTime)
    last_stage_id = Column(String)
    cleared_to_play = Column(Boolean)
    answers = Column(Text)