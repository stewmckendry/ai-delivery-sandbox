from app.db.database import SessionLocal
from app.db.db_models import IncidentReport, SymptomLog, StageLog, ActivityCheckin
from app.engines.stage_engine import StageEngine
from datetime import datetime


def get_export_bundle(user_id: str):
    db = SessionLocal()
    try:
        symptoms = db.query(SymptomLog).filter(SymptomLog.user_id == user_id).order_by(SymptomLog.timestamp.desc()).all()
        stage_log = db.query(StageLog).filter(StageLog.user_id == user_id).order_by(StageLog.timestamp.desc()).first()
        incident = db.query(IncidentReport).filter(IncidentReport.user_id == user_id).order_by(IncidentReport.timestamp.desc()).first()
        activity = db.query(ActivityCheckin).filter(ActivityCheckin.user_id == user_id).order_by(ActivityCheckin.timestamp.desc()).first()

        stage_detail = StageEngine().data
        matched = next((s for s in stage_detail.stages if s.id == stage_log.stage_id), None) if stage_log else None

        return {
            "symptoms": symptoms,
            "stage": matched,
            "incident": incident,
            "activity": activity
        }
    finally:
        db.close()