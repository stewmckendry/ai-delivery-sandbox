from app.tools.search_handlers.general import handle_general_search
from app.tools.search_handlers.jurisdiction import handle_jurisdiction_search
from app.tools.search_handlers.market import handle_market_search
from app.tools.tool_utils.web_search_logger import log_web_search
from app.db.session import get_db

class Tool:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "search_type": {"type": "string"},
                "context": {"type": "object"}
            },
            "required": ["query", "search_type"]
        }

    def run_tool(self, inputs):
        query = inputs["query"]
        search_type = inputs["search_type"]
        context = inputs.get("context", {})

        if search_type == "general":
            results = handle_general_search(query=query, context=context)
        elif search_type == "jurisdiction":
            results = handle_jurisdiction_search(query=query, context=context)
        elif search_type == "market":
            results = handle_market_search(query=query, context=context)
        else:
            raise ValueError(f"Unsupported search_type: {search_type}")

        # Log the search
        db = next(get_db())
        log_web_search(
            db,
            search_type=search_type,
            query=query,
            results_summary=results,
            tool_invoked_by="webSearch",
            user_id=context.get("user_id"),
            session_id=context.get("session_id"),
            project_id=context.get("project_id")
        )

        return results