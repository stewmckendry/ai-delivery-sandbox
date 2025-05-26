from app.tools.tool_utils.web_search_formatter import format_search_results
from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_market_search(query: str, context: dict) -> list:
    industry = context.get("industry") or context.get("project_profile", {}).get("sector")
    if industry:
        query = f"{query} in {industry} industry"

    # Add keywords to steer toward market and vendor results
    market_query = f"{query} vendors OR suppliers OR case study"
    raw_results = bing_web_search(market_query)
    return format_search_results(raw_results)