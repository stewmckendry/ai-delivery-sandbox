from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_jurisdiction_search(query: str, context: dict = None) -> list:
    location = context.get("location") if context else "government"
    if location:
        query = f"{location} {query} site:.gov OR site:.gc.ca OR site:.gov.uk"
    return bing_web_search(query)