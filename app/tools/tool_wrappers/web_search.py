from app.tools.search_handlers.general import handle_general_search
from app.tools.search_handlers.jurisdiction import handle_jurisdiction_search
from app.tools.search_handlers.market import handle_market_search
from app.tools.tool_utils.web_search_logger import log_web_search
from app.engines.memory_sync import log_tool_usage
from app.db.database import get_session
import logging

logger = logging.getLogger(__name__)

class Tool:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "search_type": {"type": "string"},
                "context": {"type": "object"},
                "input_dict": {
                    "type": "object",
                    "description": "Additional input parameters for the tool, if any"
                }
            },
            "required": ["query", "search_type"]
        }

    def run_tool(self, inputs):
        logger.info("[Tool] web_search started")

        query = inputs["query"]
        search_type = inputs["search_type"]
        input_dict = inputs.get("input_dict", {})
        search_filter = input_dict.get("search_filter", {})
        inputs = input_dict.get("inputs", {})
        logger.info(f"[Tool] web_search received query: {query}, search_type: {search_type}, context: {context}")
        
        if search_type == "general":
            results = handle_general_search(query=query, search_filter=search_filter)
        elif search_type == "jurisdiction":
            results = handle_jurisdiction_search(query=query, search_filter=search_filter)
        elif search_type == "market":
            results = handle_market_search(query=query, search_filter=search_filter)
        else:
            raise ValueError(f"Unsupported search_type: {search_type}")
        logger.info(f"[Tool] web_search results: {len(results)} entries found")
        
        # Log the search (WebSearchLog)
        db = get_session()
        log_web_search(
            db,
            search_type=search_type,
            query=query,
            results_summary=results,
            tool_invoked_by="webSearch",
            user_id=inputs.get("user_id"),
            session_id=inputs.get("session_id"),
            project_id=inputs.get("project_id")
        )
        # Log tool usage (PromptLog)
        log_tool_usage(
            "webSearch",
            f"global_context | webSearch | {search_type}",
            results,
            inputs.get("session_id"),
            inputs.get("user_id"),
            inputs
        )
        logger.info("[Tool] web_search completed")
        return results