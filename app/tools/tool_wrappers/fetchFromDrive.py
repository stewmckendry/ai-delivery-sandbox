import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.tools.tool_wrappers.base_tool import BaseTool

logger = logging.getLogger(__name__)
load_dotenv()

class Tool(BaseTool):
    def run(self, input_data: dict) -> dict:
        gate_id = input_data["gate_id"]
        artifact_id = input_data["artifact_id"]
        version = input_data["version"]

        creds_path = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH")
        if not creds_path:
            raise ValueError("Missing GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH in environment.")

        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=["https://www.googleapis.com/auth/drive"])
        drive_service = build("drive", "v3", credentials=creds)

        try:
            parent_query = f"name='gate_{gate_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            parent_resp = drive_service.files().list(q=parent_query, fields="files(id, name)").execute()
            gate_folders = parent_resp.get("files", [])
            if not gate_folders:
                raise FileNotFoundError(f"No folder found for gate_{gate_id}")

            gate_folder_id = gate_folders[0]["id"]
            sub_query = f"'{gate_folder_id}' in parents and name contains '{artifact_id}_v{version}' and mimeType='application/pdf' and trashed=false"
            file_resp = drive_service.files().list(q=sub_query, fields="files(id, name, webViewLink)").execute()
            matches = file_resp.get("files", [])

            if not matches:
                raise FileNotFoundError(f"No PDF found for artifact_id={artifact_id} v={version} in gate_{gate_id}")

            best_match = matches[0]
            return {
                "file_name": best_match["name"],
                "webViewLink": best_match["webViewLink"]
            }

        except HttpError as error:
            logger.error(f"Drive API error: {error}")
            raise RuntimeError(f"Drive API failed: {error}")

    @classmethod
    def schema(cls) -> dict:
        return {
            "type": "object",
            "properties": {
                "gate_id": {"type": "string"},
                "artifact_id": {"type": "string"},
                "version": {"type": "string"}
            },
            "required": ["gate_id", "artifact_id", "version"]
        }