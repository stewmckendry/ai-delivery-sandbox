from app.tools.tool_utils.web_search_formatter import format_search_results
from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_general_search(query: str, context: dict) -> list:
    raw_results = bing_web_search(query)
    return format_search_results(raw_results)