from clients.airtable_client import save_to_airtable, get_reflections
from clients.notion_client import save_to_notion

def save_reflection(data: dict) -> bool:
    try:
        success_airtable = save_to_airtable(data)
        success_notion = save_to_notion(data)
        return success_airtable and success_notion
    except Exception:
        return False

def get_summary(session_id: str) -> str:
    try:
        reflections = get_reflections(session_id)
        if not reflections:
            return "No reflections yet for this session."
        joined = "\n\n".join(r["text"] for r in reflections if "text" in r)
        return joined.strip()
    except Exception as e:
        raise RuntimeError(f"Error fetching summary: {str(e)}")