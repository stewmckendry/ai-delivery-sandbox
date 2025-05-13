from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Existing models omitted for brevity...

class RecoveryCheck(Base):
    __tablename__ = "recovery_check"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    timestamp = Column(DateTime)
    injury_date = Column(Date)
    symptoms = Column(Text)  # stringified dict
    source = Column(String)  # e.g., "quick_prompt"
    notes = Column(Text)