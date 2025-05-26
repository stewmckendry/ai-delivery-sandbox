import os
import requests
from urllib.parse import urlencode

def bing_web_search(query: str, count: int = 5) -> list:
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        raise ValueError("Missing BING_API_KEY in environment")

    base_url = "https://bing-web-search1.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "bing-web-search1.p.rapidapi.com"
    }
    # Build query string manually
    query_string = urlencode({
        "q": query,
        "mkt": "en-us",
        "safeSearch": "Off",
        "textFormat": "Raw",
        "freshness": "Day"
    })
    full_url = f"{base_url}?{query_string}"

    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("webPages", {}).get("value", []):
        results.append({
            "title": item.get("name"),
            "snippet": item.get("snippet"),
            "source": item.get("displayUrl"),
            "url": item.get("url"),
            "date": item.get("dateLastCrawled")
        })
    return results