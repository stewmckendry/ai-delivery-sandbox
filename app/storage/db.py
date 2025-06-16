import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.propagate = False

env_database_url = os.getenv("DATABASE_URL")
if env_database_url:
    logger.info(f"Using DATABASE_URL from environment")
    DATABASE_URL = env_database_url
else:
    logger.info(
        "DATABASE_URL not found in environment, using default: sqlite:///./health_data.db"
    )
    DATABASE_URL = "sqlite:///./health_data.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new database session after ensuring tables exist."""
    init_db()
    return SessionLocal()
