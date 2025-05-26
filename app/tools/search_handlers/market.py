from app.tools.tool_utils.web_search_formatter import format_search_results

def handle_market_search(query: str, context: dict) -> list:
    industry = context.get("industry", "infrastructure tech")
    raw_results = [
        {
            "title": f"Top vendors in {industry} sector in 2024",
            "snippet": f"A review of top-rated solutions in {industry} procurement...",
            "source": "TechInsights",
            "url": f"https://techinsights.example.com/vendors-{industry.replace(' ', '-')}",
            "date": "2024-12-01"
        }
    ]
    return format_search_results(raw_results)