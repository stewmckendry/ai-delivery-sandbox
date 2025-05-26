import os
import requests

def bing_web_search(query: str, count: int = 5) -> list:
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        raise ValueError("Missing BING_API_KEY in environment")

    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": query, "count": count}

    response = requests.get(url, headers=headers, params=params)
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