import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.db_models import TriageResponse, IncidentReport, SymptomLog, SessionLocal
from reference_loader import load_triage_map, load_stages_yaml
import json

# Establish database connection
SQL_CONN_STR = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(SQL_CONN_STR)
Session = sessionmaker(bind=engine)

def export_to_sql():
    triage_map = load_triage_map()
    stages_yaml = load_stages_yaml()

    db = SessionLocal()
    with engine.begin() as conn:
        # Export triage responses
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

        # Export incident reports
        incident_rows = db.query(IncidentReport).all()
        for row in incident_rows:
            conn.execute(
                text("""
                INSERT INTO incident_report_export (
                    user_id, injury_date, reporter_role, sport_type, age_group,
                    team_id, injury_context, symptoms, lost_consciousness,
                    seen_provider, diagnosed_concussion, still_symptomatic,
                    cleared_to_play, timestamp
                ) VALUES (
                    :user_id, :injury_date, :reporter_role, :sport_type, :age_group,
                    :team_id, :injury_context, :symptoms, :lost_consciousness,
                    :seen_provider, :diagnosed_concussion, :still_symptomatic,
                    :cleared_to_play, :timestamp
                )
                """),
                {
                    "user_id": row.user_id,
                    "injury_date": row.injury_date,
                    "reporter_role": row.reporter_role,
                    "sport_type": row.sport_type,
                    "age_group": row.age_group,
                    "team_id": row.team_id,
                    "injury_context": row.injury_context,
                    "symptoms": row.symptoms,
                    "lost_consciousness": row.lost_consciousness,
                    "seen_provider": row.seen_provider,
                    "diagnosed_concussion": row.diagnosed_concussion,
                    "still_symptomatic": row.still_symptomatic,
                    "cleared_to_play": row.cleared_to_play,
                    "timestamp": row.timestamp
                }
            )

        # Export symptom logs
        symptom_logs = db.query(SymptomLog).all()
        for row in symptom_logs:
            conn.execute(
                text("""
                INSERT INTO symptom_log_export (
                    user_id, timestamp, symptoms, log_metadata, incident_context,
                    reporter_type, sport_type, age_group, team_id
                ) VALUES (
                    :user_id, :timestamp, :symptoms, :log_metadata, :incident_context,
                    :reporter_type, :sport_type, :age_group, :team_id
                )
                """),
                {
                    "user_id": row.user_id,
                    "timestamp": row.timestamp,
                    "symptoms": row.symptoms,
                    "log_metadata": row.log_metadata,
                    "incident_context": row.incident_context,
                    "reporter_type": row.reporter_type,
                    "sport_type": row.sport_type,
                    "age_group": row.age_group,
                    "team_id": row.team_id
                }
            )
    db.close()

if __name__ == "__main__":
    export_to_sql()