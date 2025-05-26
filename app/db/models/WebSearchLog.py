from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class WebSearchLog(Base):
    __tablename__ = 'web_search_logs'

    id = Column(Integer, primary_key=True)
    search_type = Column(String)
    query = Column(String)
    results_summary = Column(JSON)
    tool_invoked_by = Column(String)
    user_id = Column(String)
    session_id = Column(String)
    project_id = Column(Integer, ForeignKey('project_profiles.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)