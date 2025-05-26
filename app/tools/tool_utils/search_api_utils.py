import os
import requests

def bing_web_search(query: str, count: int = 5) -> list:
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise ValueError("Missing SERPAPI_KEY in environment")

    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": "google",
        "api_key": api_key,
        "num": count
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "source": item.get("source") or item.get("displayed_link"),
            "url": item.get("link"),
            "date": item.get("date") or item.get("published")
        })
    return results