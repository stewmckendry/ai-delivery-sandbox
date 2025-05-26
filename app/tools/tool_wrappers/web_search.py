from app.tools.search_handlers.general import handle_general_search
from app.tools.search_handlers.jurisdiction import handle_jurisdiction_search
from app.tools.search_handlers.market import handle_market_search

class Tool:
    def validate(self, input_dict):
        if "query" not in input_dict:
            raise ValueError("Missing required field: query")
        if "search_type" not in input_dict:
            raise ValueError("Missing required field: search_type")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        query = input_dict["query"]
        search_type = input_dict["search_type"]
        context = input_dict.get("context", {})

        search_router = {
            "general": handle_general_search,
            "jurisdiction": handle_jurisdiction_search,
            "market": handle_market_search,
        }

        handler = search_router.get(search_type)
        if not handler:
            raise ValueError(f"Unsupported search type: {search_type}")

        return handler(query=query, context=context)