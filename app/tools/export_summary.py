from fastapi import APIRouter
from pydantic import BaseModel
from app.engines.epic_writer import build_fhir_bundle
from app.engines.pdf_renderer import render_pdf
from app.db.db_reader import get_tracker_and_logs
import uuid

router = APIRouter()

class ExportResponse(BaseModel):
    pdf_url: str
    fhir_bundle: dict

def upload_to_storage(pdf_path):
    """
    TODO: Replace with real cloud upload (e.g., Azure Blob, S3)
    Simulates uploading and returns a public URL
    """
    pdf_id = uuid.uuid4().hex
    return f"https://yourdomain.com/exports/summary_{pdf_id}.pdf"

@router.post("/export_summary", response_model=ExportResponse)
def export_summary(user_id: str):
    """
    Tool: export_summary
    Input: user_id (str)
    Returns: ExportResponse with PDF summary URL and FHIR bundle
    Flow:
    - Fetch user tracker and logs from DB
    - Generate FHIR bundle using epic_writer
    - Render PDF using pdf_renderer
    - Upload PDF to cloud (stubbed)
    - Return combined output for GPT or frontend display
    """
    # Fetch user tracker state and logs
    tracker, logs = get_tracker_and_logs(user_id)

    # Generate FHIR bundle
    fhir_bundle = build_fhir_bundle(tracker, logs)

    # Render PDF and upload to public storage
    pdf_path = render_pdf(user_id, tracker['state']['stage'], logs)
    pdf_url = upload_to_storage(pdf_path)

    return ExportResponse(pdf_url=pdf_url, fhir_bundle=fhir_bundle)