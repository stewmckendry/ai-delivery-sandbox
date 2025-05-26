from app.tools.search_handlers.general import handle_general_search
from app.tools.search_handlers.jurisdiction import handle_jurisdiction_search
from app.tools.search_handlers.market import handle_market_search

search_router = {
    "general": handle_general_search,
    "jurisdiction": handle_jurisdiction_search,
    "market": handle_market_search,
}

def run_web_search(query: str, search_type: str, context: dict) -> list:
    handler = search_router.get(search_type)
    if not handler:
        raise ValueError(f"Unsupported search type: {search_type}")
    return handler(query=query, context=context)