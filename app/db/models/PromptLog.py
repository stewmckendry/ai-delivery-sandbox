from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PromptLog(Base):
    __tablename__ = 'prompt_logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tool = Column(String(255))
    input_summary = Column(Text)  # Short version or hash of input
    output_summary = Column(Text)  # Short version or hash of output
    full_input_path = Column(String(1024))  # e.g., GitHub or file ref
    full_output_path = Column(String(1024))
    user_id = Column(String(255), nullable=True)
    session_id = Column(String(255), nullable=True)