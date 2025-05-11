from fastapi import APIRouter
from pydantic import BaseModel
from app.engines.epic_writer import build_fhir_bundle
from app.engines.pdf_renderer import render_pdf
from app.db.db_reader import get_tracker_and_logs
import uuid
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

router = APIRouter()

class ExportResponse(BaseModel):
    pdf_url: str
    fhir_bundle: dict

def upload_to_storage(pdf_path):
    """
    Uploads a PDF to Azure Blob Storage and returns a signed public URL
    """
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = "exports"

    blob_service = BlobServiceClient.from_connection_string(conn_str)
    blob_name = f"summary_{uuid.uuid4().hex}.pdf"
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    # Upload file
    with open(pdf_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    # Generate SAS token
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
    """
    Tool: export_summary
    Input: user_id (str)
    Returns: ExportResponse with PDF summary URL and FHIR bundle
    Flow:
    - Fetch user tracker and logs from DB
    - Generate FHIR bundle using epic_writer
    - Render PDF using pdf_renderer
    - Upload PDF to cloud (Azure Blob)
    - Return combined output for GPT or frontend display
    """
    # Fetch user tracker state and logs
    tracker, logs = get_tracker_and_logs(user_id)

    # Generate FHIR bundle
    fhir_bundle = build_fhir_bundle(tracker, logs)

    # Render PDF and upload to Azure Blob Storage
    pdf_path = render_pdf(user_id, tracker['state']['stage'], logs)
    pdf_url = upload_to_storage(pdf_path)

    return ExportResponse(pdf_url=pdf_url, fhir_bundle=fhir_bundle)