import os
import httpx

def save_to_notion(session_id: str, career_id: str, prompt_id: str, text: str) -> bool:
    notion_token = os.getenv("NOTION_API_KEY")
    notion_db = os.getenv("NOTION_REFLECTION_DB")

    if not notion_token or not notion_db:
        print("❌ Missing Notion config")
        return False

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    payload = {
        "parent": {"database_id": notion_db},
        "properties": {
            "Career": {"title": [{"text": {"content": career_id}}]},
            "Prompt": {"rich_text": [{"text": {"content": prompt_id}}]},
            "Reflection": {"rich_text": [{"text": {"content": text}}]}
        }
    }

    try:
        r = httpx.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
        if r.status_code not in [200, 201]:
            print("❌ Notion API error:", r.status_code)
            print(r.text)
            return False
        return True
    except Exception as e:
        print("❌ Notion save exception:", str(e))
        return False