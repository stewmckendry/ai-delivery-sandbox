from app.symptom_library import load_symptom_definitions
from app.db.db_models import SymptomLog
from sqlalchemy.orm import Session
from app.db.db_models import SessionLocal


def audit_symptom_schema():
    """Compare YAML symptom definitions with SymptomLog data fields."""
    db: Session = SessionLocal()
    try:
        symptom_ids_in_logs = set()
        for row in db.query(SymptomLog).all():
            try:
                symptom_data = eval(row.symptoms)
                if isinstance(symptom_data, dict):
                    symptom_ids_in_logs.update(symptom_data.keys())
            except Exception:
                continue

        defined_ids = load_symptom_definitions().keys()
        undefined = symptom_ids_in_logs - set(defined_ids)

        print("\n[SYMPTOM AUDIT REPORT]")
        if not undefined:
            print("All symptom IDs in logs are defined in YAML.")
        else:
            print("Undefined symptom IDs found in logs:")
            for uid in sorted(undefined):
                print(f" - {uid}")
    finally:
        db.close()