from fastapi import APIRouter
from pydantic import BaseModel
from app.engines.epic_writer import build_fhir_bundle
from app.engines.pdf_renderer import render_pdf
from app.db.db_reader import get_export_bundle
from app.db.db_models import ConcussionAssessment
from app.db.database import SessionLocal
import uuid
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

router = APIRouter()

class ExportResponse(BaseModel):
    pdf_url: str
    fhir_bundle: dict

def upload_to_storage(content: str):
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "exports"

    blob_service = BlobServiceClient.from_connection_string(conn_str)
    blob_name = f"summary_{uuid.uuid4().hex}.pdf"
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    blob_client.upload_blob(content.encode("utf-8"), overwrite=True)

    sas_token = generate_blob_sas(
        account_name="concussionexports",
        container_name=container_name,
        blob_name=blob_name,
        account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY"),
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )

    return f"https://concussionexports.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

@router.post("/export_summary", response_model=ExportResponse)
def export_summary(user_id: str):
    bundle = get_export_bundle(user_id)
    symptoms = bundle["symptoms"]
    stage = bundle["stage"]
    incident = bundle["incident"]
    activity = bundle["activity"]

    db = SessionLocal()
    try:
        assessment = db.query(ConcussionAssessment).filter_by(user_id=user_id).order_by(ConcussionAssessment.timestamp.desc()).first()
    finally:
        db.close()

    pdf_str = render_pdf(user_id, symptoms, stage, incident, activity)
    pdf_url = upload_to_storage(pdf_str)
    fhir = build_fhir_bundle(symptoms, stage, incident, assessment, activity)

    return ExportResponse(pdf_url=pdf_url, fhir_bundle=fhir)