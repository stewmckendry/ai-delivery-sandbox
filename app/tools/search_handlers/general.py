from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_general_search(query: str, context: dict = None) -> list:
    raw_results = bing_web_search(query)
    return raw_results