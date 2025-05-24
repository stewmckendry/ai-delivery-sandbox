from typing import Dict
from pydantic import BaseModel, parse_obj_as
import os
from datetime import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# Define OAuth scope and credentials location
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH")
FOLDER_NAME = "PolicyGPT"

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

        # Authenticate and build Drive service
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=creds)

        # Create or find target folder structure (NOTE: project_id is not yet implemented in schema)
        folder_id = self._get_or_create_folder_structure(service, data)

        # Prepare filename with versioning timestamp
        filename = f"{data.artifact_id}_v{data.version}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.md"
        media = MediaInMemoryUpload(data.final_markdown.encode("utf-8"), mimetype="text/markdown")

        # Upload the file to Google Drive
        file_metadata = {
            "name": filename,
            "parents": [folder_id],
        }
        file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

        return OutputSchema(drive_url=file["webViewLink"]).dict()

    def _get_or_create_folder_structure(self, service, data):
        # Helper to find or create folder in Drive
        def find_or_create(name, parent=None):
            query = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
            if parent:
                query += f" and '{parent}' in parents"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            files = results.get("files", [])
            if files:
                return files[0]["id"]
            metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
            if parent:
                metadata["parents"] = [parent]
            file = service.files().create(body=metadata, fields="id").execute()
            return file["id"]

        # Folder path logic: PolicyGPT/gate_<gate_id>/<artifact_id>
        # Future: Add project_id at higher level once schema supports it
        root_id = find_or_create(FOLDER_NAME)
        gate_folder = find_or_create(f"gate_{data.gate_id}", parent=root_id)
        artifact_folder = find_or_create(data.artifact_id, parent=gate_folder)
        return artifact_folder