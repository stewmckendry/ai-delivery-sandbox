from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class SymptomLog(Base):
    __tablename__ = "symptom_log"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    symptom_id = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # New metadata fields for dashboard
    reporter_type = Column(String)       # e.g., "self", "coach", "parent"
    incident_context = Column(String)    # e.g., "practice", "game"
    sport_type = Column(String)          # e.g., "soccer", "hockey"
    age_group = Column(String)           # e.g., "U14", "High School"
    team_id = Column(String)             # Optional program/team grouping