import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.db_models import TriageResponse, SessionLocal
from reference_loader import load_triage_map, load_stages_yaml

# Establish database connection
SQL_CONN_STR = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(SQL_CONN_STR)
Session = sessionmaker(bind=engine)

def export_to_sql():
    triage_map = load_triage_map()
    stages_yaml = load_stages_yaml()

    db = SessionLocal()
    with engine.begin() as conn:
        # Export all triage responses
        triage_rows = db.query(TriageResponse).all()
        for row in triage_rows:
            conn.execute(
                text("""
                INSERT INTO triage_response_export (
                    user_id, question_id, question_text, answer, timestamp
                ) VALUES (
                    :user_id, :question_id, :question_text, :answer, :timestamp
                )
                """),
                {
                    "user_id": row.user_id,
                    "question_id": row.question_id,
                    "question_text": row.question_text,
                    "answer": row.answer,
                    "timestamp": row.timestamp
                }
            )
    db.close()

if __name__ == "__main__":
    export_to_sql()