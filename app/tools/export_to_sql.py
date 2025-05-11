import os
from sqlalchemy import create_engine, text
from app.db.db_reader import get_all_tracker_logs
from reference_loader import load_triage_map, load_stages_yaml

# Establish database connection
SQL_CONN_STR = os.getenv("AZURE_SQL_CONNECTION_STRING")
engine = create_engine(SQL_CONN_STR)

def export_to_sql():
    tracker_logs = get_all_tracker_logs()
    triage_map = load_triage_map()
    stages_yaml = load_stages_yaml()

    with engine.begin() as conn:
        for tracker, logs in tracker_logs:
            user_id = tracker['user_id']
            current_stage = tracker['state']['stage']
            last_updated = tracker['updated_at']
            triage_level = triage_map.get(tracker['state'].get('triage_id', ''), {}).get('level', 'unknown')

            conn.execute(
                text("""
                INSERT INTO tracker_export (user_id, current_stage, last_updated, triage_level)
                VALUES (:user_id, :stage, :updated, :level)
                """),
                {"user_id": user_id, "stage": current_stage, "updated": last_updated, "level": triage_level}
            )

            for log in logs:
                conn.execute(
                    text("""
                    INSERT INTO symptom_log_export (user_id, symptom_id, severity, timestamp)
                    VALUES (:user_id, :symptom_id, :severity, :timestamp)
                    """),
                    {
                        "user_id": user_id,
                        "symptom_id": log['symptom_id'],
                        "severity": log['severity'],
                        "timestamp": log['timestamp']
                    }
                )

if __name__ == "__main__":
    export_to_sql()