import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use env variable for secure connection string
DATABASE_URL = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
