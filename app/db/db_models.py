from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SymptomLog(Base):
    __tablename__ = "symptom_log_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    timestamp = Column(DateTime)
    symptoms = Column(Text)
    log_metadata = Column(Text)  # Renamed from 'metadata'
    incident_context = Column(String)
    reporter_type = Column(String)
    sport_type = Column(String)
    age_group = Column(String)
    team_id = Column(String)
    extra_notes = Column(Text)  # new: capture freeform notes or unlisted symptoms

class TrackerMetadata(Base):
    __tablename__ = "tracker_export"

    user_id = Column(String, primary_key=True)
    injury_date = Column(DateTime)
    last_checkin_time = Column(DateTime)
    last_stage_id = Column(String)
    cleared_to_play = Column(Boolean)
    answers = Column(Text)

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