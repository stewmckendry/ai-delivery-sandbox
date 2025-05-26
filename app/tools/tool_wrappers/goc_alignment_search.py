from app.tools.search_handlers.goc_alignment import handle_goc_alignment_search
from app.tools.tool_utils.web_search_logger import log_web_search

def run_tool(input_dict):
    query = input_dict.get("query")
    user_id = input_dict.get("user_id")
    session_id = input_dict.get("session_id")
    project_id = input_dict.get("project_id")

    if not query:
        return {"error": "Missing required field: query"}

    results = handle_goc_alignment_search(query)

    log_web_search(
        query=query,
        search_type="goc_alignment",
        results=results,
        user_id=user_id,
        session_id=session_id,
        project_id=project_id,
    )

    return {"results": results}