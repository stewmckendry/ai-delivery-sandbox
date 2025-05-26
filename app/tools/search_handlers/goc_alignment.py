from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_goc_alignment_search(query: str, context: dict = None) -> list:
    """
    Executes a government-aligned web search restricted to .gc.ca domains.
    Example: query='open government strategy' -> search: 'open government strategy site:.gc.ca'
    """
    scoped_query = f"{query} site:.gc.ca"
    return bing_web_search(scoped_query)