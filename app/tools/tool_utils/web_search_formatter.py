def format_search_results(raw_results: list) -> list:
    formatted = []
    for r in raw_results:
        formatted.append({
            "title": r.get("title", ""),
            "snippet": r.get("snippet", ""),
            "source": r.get("source", ""),
            "date": r.get("date", ""),
            "url": r.get("url", "")
        })
    return formatted