from app.tools.tool_utils.web_search_formatter import format_search_results
from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_jurisdiction_search(query: str, context: dict) -> list:
    location = context.get("location") or context.get("project_profile", {}).get("region")
    if location:
        query = f"{location} {query}"
    
    # Focus on government/policy keywords
    scoped_query = f"{query} site:.gov OR site:.gc.ca OR site:.gov.uk"
    raw_results = bing_web_search(scoped_query)
    return format_search_results(raw_results)