from sqlalchemy import Column, String, Date, Integer, Text, TIMESTAMP, Numeric
from app.db.database import Base
import datetime

class ProjectProfile(Base):
    __tablename__ = "project_profile"

    project_id = Column(String, primary_key=True)
    title = Column(Text)
    sponsor = Column(Text)
    project_type = Column(String)
    total_budget = Column(Numeric)
    start_date = Column(Date)
    end_date = Column(Date)
    strategic_alignment = Column(Text)
    current_gate = Column(Integer)
    scope_summary = Column(Text)
    key_stakeholders = Column(Text)
    major_risks = Column(Text)
    resource_summary = Column(Text)
    last_updated = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
