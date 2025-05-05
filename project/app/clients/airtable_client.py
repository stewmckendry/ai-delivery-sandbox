import os
import httpx

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "CareerReflections")
AIRTABLE_API_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def save_to_airtable(data: dict) -> bool:
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("[Airtable] Missing credentials")
        return False
    try:
        record = {"fields": {
            "session_id": data["session_id"],
            "career_id": data["career_id"],
            "prompt_id": data["prompt_id"],
            "text": data["text"]
        }}
        response = httpx.post(AIRTABLE_API_URL, json=record, headers=HEADERS)
        return response.status_code == 200 or response.status_code == 201
    except Exception as e:
        print(f"[Airtable] Error saving: {e}")
        return False

def get_reflections(session_id: str) -> list:
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("[Airtable] Missing credentials")
        return []
    try:
        params = {
            "filterByFormula": f'{{session_id}}="{session_id}"'
        }
        response = httpx.get(AIRTABLE_API_URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            return [rec["fields"] for rec in response.json().get("records", [])]
        return []
    except Exception as e:
        print(f"[Airtable] Error fetching: {e}")
        return []