from sqlalchemy.orm import Session
from app.db.db_models import SymptomLog, StageLog, IncidentReport
from app.db.database import SessionLocal


def get_export_bundle(user_id: str):
    db: Session = SessionLocal()
    try:
        symptoms = db.query(SymptomLog).filter_by(user_id=user_id).order_by(SymptomLog.timestamp).all()
        stage = db.query(StageLog).filter_by(user_id=user_id).order_by(StageLog.timestamp.desc()).first()
        incident = db.query(IncidentReport).filter_by(user_id=user_id).first()

        symptom_logs = []
        for row in symptoms:
            import json
            parsed = json.loads(row.symptoms)
            for sid, sev in parsed.items():
                symptom_logs.append({
                    "symptom_id": sid,
                    "severity": sev,
                    "timestamp": row.timestamp.isoformat(),
                    "reporter_type": row.reporter_type,
                    "incident_context": row.incident_context,
                    "sport_type": row.sport_type,
                    "age_group": row.age_group,
                    "team_id": row.team_id
                })

        return {
            "incident": incident,
            "stage": stage.inferred_stage if stage else None,
            "symptoms": symptom_logs
        }
    finally:
        db.close()