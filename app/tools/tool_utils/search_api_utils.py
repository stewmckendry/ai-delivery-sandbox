import os
import requests

def bing_web_search(query: str, count: int = 5) -> list:
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        raise ValueError("Missing BING_API_KEY in environment")

    url = "https://bing-web-search1.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "bing-web-search1.p.rapidapi.com"
    }
    params = {
        "q": query,
        "mkt": "en-us",
        "safeSearch": "Off",
        "textFormat": "Raw",
        "freshness": "Day"
    }

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