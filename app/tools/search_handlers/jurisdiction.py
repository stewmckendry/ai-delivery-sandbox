from app.tools.tool_utils.web_search_formatter import format_search_results

def handle_jurisdiction_search(query: str, context: dict) -> list:
    # This would eventually parse for jurisdiction or location cues
    location = context.get("location", "Canada")
    raw_results = [
        {
            "title": f"How {location} regulates digital identity",
            "snippet": f"{location} has adopted a national strategy for digital identity...",
            "source": "GovTech",
            "url": f"https://govtech.example.com/digital-id-{location.lower()}",
            "date": "2024-08-15"
        }
    ]
    return format_search_results(raw_results)