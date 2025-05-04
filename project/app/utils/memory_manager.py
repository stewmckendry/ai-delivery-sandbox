from clients.airtable_client import save_to_airtable
from clients.notion_client import save_to_notion

def save_reflection(data: dict) -> bool:
    try:
        success_airtable = save_to_airtable(data)
        success_notion = save_to_notion(data)
        return success_airtable and success_notion
    except Exception:
        return False