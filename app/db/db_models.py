from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SymptomLog(Base):
    __tablename__ = "symptom_log_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    symptom_id = Column(String, nullable=False)
    symptom_input = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    log_metadata = Column(Text, nullable=True)

class TriageResponse(Base):
    __tablename__ = "triage_response_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    question_id = Column(String)
    question_text = Column(Text)
    answer = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class IncidentReport(Base):
    __tablename__ = "incident_report_export"

    user_id = Column(String, primary_key=True)
    injury_date = Column(DateTime)
    reporter_role = Column(String)
    sport_type = Column(String)
    age_group = Column(String)
    team_id = Column(String)
    injury_context = Column(String)
    symptoms = Column(Text)
    lost_consciousness = Column(Boolean)
    seen_provider = Column(Boolean)
    diagnosed_concussion = Column(Boolean)
    still_symptomatic = Column(Boolean)
    cleared_to_play = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ConcussionAssessment(Base):
    __tablename__ = "concussion_assessment_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    concussion_likely = Column(Boolean)
    red_flags_present = Column(Boolean)
    summary = Column(Text)

class StageLog(Base):
    __tablename__ = "stage_result_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    inferred_stage = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)