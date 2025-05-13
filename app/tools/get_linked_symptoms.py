from fastapi import APIRouter, HTTPException
from app.db.database import SessionLocal
from app.db.db_models import SymptomLog

router = APIRouter()

@router.get("/get_linked_symptoms/{user_id}", tags=["symptoms"])
def get_linked_symptoms(user_id: str):
    db = SessionLocal()
    try:
        logs = db.query(SymptomLog).filter_by(user_id=user_id).order_by(SymptomLog.timestamp.desc()).all()
        result = [
            {
                "symptom_id": row.symptom_id,
                "score": row.score,
                "notes": row.notes,
                "timestamp": row.timestamp.isoformat()
            }
            for row in logs
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch symptoms: {str(e)}")
    finally:
        db.close()