from sqlalchemy import create_engine
from app.db.db_models import Base
import os

# Connect using the AZURE_SQL_CONNECTION_STRING env var
DATABASE_URL = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(DATABASE_URL)

print("Creating tables using metadata from db_models.py...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")