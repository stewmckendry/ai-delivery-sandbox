from fastapi import APIRouter
from app.db.db_reader import get_export_bundle
from app.engines.epic_writer import build_fhir_bundle
from app.engines.pdf_renderer import render_pdf

router = APIRouter()

@router.get("/export_summary")
def export_summary(user_id: str):
    bundle = get_export_bundle(user_id)
    fhir = build_fhir_bundle(bundle["symptoms"], bundle.get("stage"), bundle.get("incident"))
    pdf = render_pdf(
        bundle["symptoms"],
        bundle.get("stage"),
        context={
            "team_id": bundle["incident"].team_id if bundle.get("incident") else None,
            "age_group": bundle["incident"].age_group if bundle.get("incident") else None,
            "sport_type": bundle["incident"].sport_type if bundle.get("incident") else None,
            "reporter_type": bundle["incident"].reporter_role if bundle.get("incident") else None,
            "incident_context": bundle["incident"].injury_context if bundle.get("incident") else None,
        }
    )
    return {"pdf_html": pdf, "fhir_bundle": fhir}