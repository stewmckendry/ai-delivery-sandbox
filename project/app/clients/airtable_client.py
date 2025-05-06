import os
import httpx

def save_to_airtable(data: dict) -> bool:
    airtable_token = os.getenv("AIRTABLE_API_KEY")
    airtable_base = os.getenv("AIRTABLE_BASE_ID")
    table_name = "Table 1"

    if not airtable_token or not airtable_base:
        print("❌ Missing Airtable config")
        return False

    headers = {
        "Authorization": f"Bearer {airtable_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "records": [
            {
                "fields": {
                    "session_id": data.get("session_id"),
                    "career_id": data.get("career_id"),
                    "prompt_id": data.get("prompt_id"),
                    "text": data.get("text"),
                    "timestamp": data.get("timestamp")
                }
            }
        ]
    }

    try:
        url = f"https://api.airtable.com/v0/{airtable_base}/{table_name}"
        r = httpx.post(url, headers=headers, json=payload)
        if r.status_code not in [200, 201]:
            print("❌ Airtable API error:", r.status_code)
            print(r.text)
            return False
        return True
    except Exception as e:
        print("❌ Airtable save exception:", str(e))
        return False

def get_reflection(session_id: str) -> str:
    airtable_token = os.getenv("AIRTABLE_API_KEY")
    airtable_base = os.getenv("AIRTABLE_BASE_ID")
    table_name = "Table 1"

    if not airtable_token or not airtable_base:
        print("❌ Missing Airtable config")
        return ""

    headers = {
        "Authorization": f"Bearer {airtable_token}"}

    url = f"https://api.airtable.com/v0/{airtable_base}/{table_name}?filterByFormula=SEARCH(%22{session_id}%22%2C+%7Bsession_id%7D)"
    try:
        r = httpx.get(url, headers=headers)
        if r.status_code != 200:
            print("❌ Airtable fetch error:", r.status_code)
            print(r.text)
            return ""

        records = r.json().get("records", [])
        if not records:
            return ""

        # Return the text field of the latest record (assumes sorted by createdTime)
        return records[0]["fields"].get("text", "")
    except Exception as e:
        print("❌ Airtable get_reflection exception:", str(e))
        return ""