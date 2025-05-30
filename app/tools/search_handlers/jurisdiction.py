from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_jurisdiction_search(query: str, search_filter: dict = None) -> list:
    location = search_filter.get("location") if search_filter else "government"
    if location:
        query = f"{location} {query} site:.gov OR site:.gc.ca OR site:.gov.uk"
    return bing_web_search(query)