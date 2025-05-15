from fastapi import APIRouter
from pydantic import BaseModel
from app.engines.epic_writer import build_fhir_bundle
from app.engines.pdf_renderer import render_pdf
from app.db.db_reader import get_export_bundle
from app.db.db_models import ConcussionAssessment
from app.db.database import SessionLocal

router = APIRouter()

class ExportRequest(BaseModel):
    user_id: str

class ExportResponse(BaseModel):
    pdf_url: str
    fhir_bundle: dict

@router.post("/export_summary", response_model=ExportResponse)
def export_summary(req: ExportRequest):
    user_id = req.user_id
    bundle = get_export_bundle(user_id)
    symptoms = bundle["symptoms"]
    incident = bundle["incident"]
    activity = bundle["activity"]
    stage = bundle["stage"]

    db = SessionLocal()
    try:
        assessment = db.query(ConcussionAssessment).filter_by(user_id=user_id).order_by(ConcussionAssessment.timestamp.desc()).first()
    finally:
        db.close()

    pdf_url = render_pdf({
        "user_id": user_id,
        "symptoms": symptoms,
        "incident": incident,
        "activity": activity,
        "stage": stage
    })
    fhir = build_fhir_bundle(symptoms, stage, incident, assessment, activity)

    return ExportResponse(pdf_url=pdf_url, fhir_bundle=fhir)