import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Central DB URL resolution
DB_URL = os.getenv("DATABASE_URL", "sqlite:///policy_gpt.db")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from app.db.models import PromptLog, SessionSnapshot  # Local import to avoid circular refs
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()