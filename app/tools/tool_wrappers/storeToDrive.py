from typing import Dict
from pydantic import BaseModel, parse_obj_as
import os
from datetime import datetime
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH")
FOLDER_ID = "1XFwEEEArV_sXcN8TXxd4VUnSOdKuQdnr"  # Explicitly use shared PolicyGPT folder
SHARE_WITH = ["stewart.mckendry@gmail.com"]

class InputSchema(BaseModel):
    final_markdown: str
    artifact_id: str
    gate_id: str
    version: str
    title: str

class OutputSchema(BaseModel):
    drive_url: str

class Tool:
    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(InputSchema, input_dict)

        logger.info("Authenticating with Google Drive using service account JSON at: %s", SERVICE_ACCOUNT_FILE)
        if not SERVICE_ACCOUNT_FILE:
            raise EnvironmentError("Missing GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH in environment.")

        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        # Build subfolder structure under shared folder ID
        folder_id = self._get_or_create_subfolders(service, FOLDER_ID, data)

        filename = f"{data.artifact_id}_v{data.version}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.md"
        logger.info("Uploading file: %s", filename)
        media = MediaInMemoryUpload(data.final_markdown.encode("utf-8"), mimetype="text/markdown")
        file_metadata = {
            "name": filename,
            "parents": [folder_id],
        }
        file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

        # Share file with configured emails
        for email in SHARE_WITH:
            permission = {
                'type': 'user',
                'role': 'reader',
                'emailAddress': email
            }
            service.permissions().create(fileId=file["id"], body=permission, sendNotificationEmail=False).execute()

        logger.info("File uploaded successfully with webViewLink: %s", file["webViewLink"])
        return OutputSchema(drive_url=file["webViewLink"]).dict()

    def _get_or_create_subfolders(self, service, root_id, data):
        def find_or_create(name, parent):
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])
            if files:
                return files[0]["id"]
            metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]}
            file = service.files().create(body=metadata, fields="id").execute()
            return file["id"]

        gate_folder = find_or_create(f"gate_{data.gate_id}", root_id)
        artifact_folder = find_or_create(data.artifact_id, gate_folder)
        return artifact_folder