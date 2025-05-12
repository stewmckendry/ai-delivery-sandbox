from fastapi import APIRouter
from app.engines.pdf_renderer import render_pdf
from app.engines.epic_writer import build_fhir_bundle
from app.db.db_reader import get_export_bundle

router = APIRouter()

@router.get("/export_summary")
def export_summary(user_id: str):
    bundle = get_export_bundle(user_id)
    symptoms = bundle["symptoms"]
    stage = bundle["stage"]
    incident = bundle["incident"]

    pdf = render_pdf(user_id, symptoms, stage)
    fhir = build_fhir_bundle(symptoms, stage, incident)

    return {"pdf": pdf, "fhir": fhir}