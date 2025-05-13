from app.db.database import SessionLocal
from app.db.db_models import SymptomLog, StageLog, IncidentReport

def get_export_bundle(user_id: str):
    db = SessionLocal()
    try:
        symptoms = db.query(SymptomLog).filter_by(user_id=user_id).order_by(SymptomLog.timestamp).all()
        stage = db.query(StageLog).filter_by(user_id=user_id).order_by(StageLog.timestamp.desc()).first()
        incident = db.query(IncidentReport).filter_by(user_id=user_id).first()

        symptom_logs = []
        for row in symptoms:
            entry = {
                "symptom_id": row.symptom_id,
                "severity": row.score,
                "timestamp": row.timestamp.isoformat(),
                "notes": row.notes,
                "source": "canonical" if row.symptom_id != "other" else "other"
            }
            if incident:
                entry.update({
                    "reporter_type": incident.reporter_type,
                    "incident_context": incident.injury_context,
                    "sport_type": incident.sport_type,
                    "age_group": incident.age_group,
                    "team_id": incident.team_id
                })
            symptom_logs.append(entry)

        return {
            "symptoms": symptom_logs,
            "stage": stage,
            "incident": incident
        }
    finally:
        db.close()