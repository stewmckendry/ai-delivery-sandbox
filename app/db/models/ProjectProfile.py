from sqlalchemy import Column, String, Date, Integer, Text, TIMESTAMP, Numeric
from app.db.database import Base
import datetime

class ProjectProfile(Base):
    __tablename__ = "project_profile"

    project_id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    sponsor = Column(Text, nullable=True)
    project_type = Column(String, nullable=True)
    total_budget = Column(Numeric, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    strategic_alignment = Column(Text, nullable=True)
    current_gate = Column(Integer, nullable=True)
    scope_summary = Column(Text, nullable=True)
    key_stakeholders = Column(Text, nullable=True)
    major_risks = Column(Text, nullable=True)
    resource_summary = Column(Text, nullable=True)
    last_updated = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)