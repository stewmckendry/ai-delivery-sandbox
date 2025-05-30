from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_market_search(query: str, search_filter: dict = None) -> list:
    sector = search_filter.get("industry") if search_filter else "government"
    if sector:
        query = f"{query} {sector} vendors OR suppliers OR case study"
    return bing_web_search(query)