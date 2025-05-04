def save_to_airtable(data: dict) -> bool:
    print("[Airtable] Saving:", data)
    return True

def get_reflections(session_id: str) -> list:
    print(f"[Airtable] Fetching reflections for {session_id}")
    return [
        {"text": "I enjoy solving problems with code."},
        {"text": "I could see myself doing this as a job."}
    ]