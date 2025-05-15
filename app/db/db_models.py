from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class IncidentReport(Base):
    __tablename__ = "incident_report_export"
    user_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    reporter_role = Column(String)
    sport_type = Column(String)
    age_group = Column(String)
    team_id = Column(String)
    injury_date = Column(DateTime)
    injury_context = Column(String)
    symptoms = Column(JSON)
    lost_consciousness = Column(Boolean)
    seen_provider = Column(Boolean)
    diagnosed_concussion = Column(Boolean)
    still_symptomatic = Column(Boolean)
    cleared_to_play = Column(Boolean)

class TriageResponse(Base):
    __tablename__ = "triage_response_export"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    question_id = Column(String)
    question_text = Column(Text)
    answer = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SymptomLog(Base):
    __tablename__ = "symptom_log_export"
    user_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    symptom_id = Column(String, primary_key=True)
    symptom_input = Column(String)
    score = Column(Integer)
    notes = Column(String)
    log_metadata = Column(Text)

class ActivityCheckin(Base):
    __tablename__ = "activity_checkin_export"
    user_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    stage_attempted = Column(String)
    symptoms_reported = Column(JSON)
    symptoms_worsened = Column(Boolean)
    notes = Column(String)

class StageLog(Base):
    __tablename__ = "stage_result_export"
    user_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    stage_id = Column(String)
    stage_name = Column(String)
    mild_days = Column(Integer)
    max_score_today = Column(Integer)
    recent_mild_day = Column(DateTime)
    inference_mode = Column(String)
    matched_factors = Column(JSON)

class ConcussionAssessment(Base):
    __tablename__ = "concussion_assessment_export"
    user_id = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    concussion_likely = Column(Boolean)
    red_flags = Column(JSON)
    moderate_symptoms = Column(JSON)
    summary = Column(String)

class SymptomLink(Base):
    __tablename__ = "symptom_link"
    user_phrase = Column(String, primary_key=True)
    matched_symptom = Column(String)
    category = Column(String)
    score = Column(Integer)
    notes = Column(String)