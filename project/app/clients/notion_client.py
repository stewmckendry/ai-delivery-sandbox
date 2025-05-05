import os
import httpx
import datetime

NOTION_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1/pages"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def save_to_notion(data: dict) -> bool:
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("[Notion] Missing credentials")
        return False
    try:
        payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Career": {"title": [{"text": {"content": data["career_id"]}}]},
                "Prompt": {"rich_text": [{"text": {"content": data["prompt_id"]}}]},
                "Reflection": {"rich_text": [{"text": {"content": data["text"]}}]},
                "Session": {"rich_text": [{"text": {"content": data["session_id"]}}]},
                "Timestamp": {"date": {"start": datetime.datetime.utcnow().isoformat()}}
            }
        }
        response = httpx.post(NOTION_API_URL, json=payload, headers=HEADERS)
        return response.status_code == 200 or response.status_code == 201
    except Exception as e:
        print(f"[Notion] Error saving: {e}")
        return False