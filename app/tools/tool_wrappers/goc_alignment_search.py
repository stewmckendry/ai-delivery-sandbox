from app.tools.search_handlers.goc_alignment import handle_goc_alignment_search
from app.tools.tool_utils.web_search_logger import log_web_search
from app.db.database import get_session

class Tool:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "context": {"type": "object"}
            },
            "required": ["query"]
        }

    def run_tool(self, inputs):
        query = inputs.get("query")
        context = inputs.get("context", {})

        if not query:
            raise ValueError("Missing required field: query")

        results = handle_goc_alignment_search(query)

        db = get_session()
        log_web_search(
            db,
            query=query,
            search_type="goc_alignment",
            results_summary=results,
            tool_invoked_by="goc_alignment_search",
            user_id=context.get("user_id"),
            session_id=context.get("session_id"),
            project_id=context.get("project_id") or context.get("project_profile", {}).get("project_id")
        )

        return {"results": results}