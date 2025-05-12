from fastapi import APIRouter
from app.engines.pdf_renderer import render_pdf
from app.engines.epic_writer import build_fhir_bundle
from app.db.db_reader import get_export_bundle
from app.db.db_models import ConcussionAssessment
from app.db.database import SessionLocal

router = APIRouter()

@router.get("/export_summary")
def export_summary(user_id: str):
    bundle = get_export_bundle(user_id)
    symptoms = bundle["symptoms"]
    stage = bundle["stage"]
    incident = bundle["incident"]

    db = SessionLocal()
    try:
        assessment = db.query(ConcussionAssessment).filter_by(user_id=user_id).order_by(ConcussionAssessment.timestamp.desc()).first()
    finally:
        db.close()

    pdf = render_pdf(user_id, symptoms, stage, incident)
    fhir = build_fhir_bundle(symptoms, stage, incident, assessment)

    return {"pdf": pdf, "fhir": fhir}