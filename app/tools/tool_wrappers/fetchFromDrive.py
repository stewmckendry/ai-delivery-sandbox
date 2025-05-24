from typing import Dict
from pydantic import BaseModel, parse_obj_as
import os
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCOPES = ["https://www.googleapis.com/auth/drive"]

class InputSchema(BaseModel):
    artifact_id: str
    gate_id: str
    version: str

class OutputSchema(BaseModel):
    file_name: str
    webViewLink: str

class Tool:
    def run_tool(self, input_dict: Dict) -> Dict:
        data = parse_obj_as(InputSchema, input_dict)

        creds_path = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH")
        if not creds_path:
            raise EnvironmentError("Missing GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON_PATH in environment.")

        logger.info("Authenticating with Google Drive using service account JSON at: %s", creds_path)
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        drive_service = build("drive", "v3", credentials=creds)

        try:
            gate_query = f"name='gate_{data.gate_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            gate_resp = drive_service.files().list(q=gate_query, fields="files(id, name)").execute()
            gate_folders = gate_resp.get("files", [])
            if not gate_folders:
                raise FileNotFoundError(f"No folder found for gate_{data.gate_id}")
            gate_folder_id = gate_folders[0]["id"]

            artifact_query = f"'{gate_folder_id}' in parents and name='{data.artifact_id}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            artifact_resp = drive_service.files().list(q=artifact_query, fields="files(id, name)").execute()
            artifact_folders = artifact_resp.get("files", [])
            if not artifact_folders:
                raise FileNotFoundError(f"No folder for artifact_id {data.artifact_id} in gate_{data.gate_id}")
            artifact_folder_id = artifact_folders[0]["id"]

            pdf_query = f"'{artifact_folder_id}' in parents and name contains '{data.artifact_id}_v{data.version}' and mimeType='application/pdf' and trashed=false"
            pdf_resp = drive_service.files().list(q=pdf_query, fields="files(id, name, webViewLink)").execute()
            matches = pdf_resp.get("files", [])

            if not matches:
                raise FileNotFoundError(f"No PDF found for artifact_id={data.artifact_id} v={data.version}")

            match = matches[0]
            return OutputSchema(file_name=match["name"], webViewLink=match["webViewLink"]).dict()

        except HttpError as error:
            logger.error(f"Drive API error: {error}")
            raise RuntimeError(f"Drive API failed: {error}")