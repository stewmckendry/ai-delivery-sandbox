from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.db_models import SymptomLog, TriageResponse, SessionLocal

router = APIRouter()

@router.get("/get_linked_symptoms/{user_id}")
def get_linked_symptoms(user_id: str):
    db: Session = SessionLocal()
    try:
        # Try latest symptom log first
        log = db.query(SymptomLog).filter_by(user_id=user_id).order_by(SymptomLog.timestamp.desc()).first()
        if log:
            import json
            parsed = json.loads(log.symptoms)
            return {"source": "SymptomLog", "symptoms": list(parsed.keys())}

        # Fallback to triage responses
        triage_qas = db.query(TriageResponse).filter_by(user_id=user_id).all()
        for row in triage_qas:
            if row.question_id == "symptoms":
                try:
                    ids = list(eval(row.answer).keys())
                    return {"source": "TriageResponse", "symptoms": ids}
                except:
                    continue
        return {"source": "none", "symptoms": []}
    finally:
        db.close()