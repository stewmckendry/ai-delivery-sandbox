from app.tools.tool_utils.search_api_utils import bing_web_search

def handle_market_search(query: str, context: dict = None) -> list:
    sector = context.get("industry") if context else "government"
    if sector:
        query = f"{query} {sector} vendors OR suppliers OR case study"
    return bing_web_search(query)