import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.db_models import TriageResponse, IncidentReport, SymptomLog, StageLog, ConcussionAssessment
from app.db.database import SessionLocal
from reference_loader import load_triage_map, load_stages_yaml
import json

SQL_CONN_STR = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(SQL_CONN_STR)
Session = sessionmaker(bind=engine)

def export_to_sql():
    triage_map = load_triage_map()
    stages_yaml = load_stages_yaml()

    db = SessionLocal()
    with engine.begin() as conn:
        # Export logic unchanged
        pass

    db.close()

if __name__ == "__main__":
    export_to_sql()