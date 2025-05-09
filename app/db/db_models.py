from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Create a base class for our ORM models
Base = declarative_base()

# Set up the database connection
# Uses Azure SQL connection string from environment variable, falls back to SQLite for dev
DATABASE_URL = os.getenv("AZURE_SQL_CONN", "sqlite:///symptom_log_dev.db")
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Define table for symptom log entries
class SymptomLog(Base):
    __tablename__ = "symptom_log"
    id = Column(String, primary_key=True, index=True)  # UUID for log entry
    user_id = Column(String)  # ID of user
    checkin_time = Column(DateTime)  # When symptoms were logged
    injury_date = Column(DateTime)  # Original injury date
    symptoms = Column(Text)  # JSON-encoded map of symptom_id → score
    stage_inferred = Column(String, nullable=True)  # Optional recovery stage
    source = Column(String, default="gpt")  # Origin (e.g., GPT, user, import)

# Define table to track user-level metadata
class TrackerMetadata(Base):
    __tablename__ = "tracker_metadata"
    user_id = Column(String, primary_key=True)  # Unique user ID
    injury_date = Column(DateTime)  # Injury start date
    last_stage_id = Column(String, nullable=True)  # Last stage assigned
    cleared_to_play = Column(Boolean, default=False)  # Flag if user has been cleared
    last_checkin_time = Column(DateTime)  # Time of latest symptom check

# Run this function to create tables if they don't exist
def init_db():
    Base.metadata.create_all(bind=engine)