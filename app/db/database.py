import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import PromptLog, SessionSnapshot
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Update this path or use DATABASE_URL env var
DB_URL = os.getenv("DATABASE_URL", "sqlite:///policy_gpt.db")

def init_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    return Session()