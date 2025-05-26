import os
import requests

def bing_web_search(query: str, count: int = 5) -> list:
    api_key = os.getenv("BING_API_KEY")
    if not api_key:
        raise ValueError("Missing BING_API_KEY in environment")

    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }
    params = {
        "q": query,
        "pageNumber": 1,
        "pageSize": count,
        "autoCorrect": True
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("value", []):
        results.append({
            "title": item.get("title"),
            "snippet": item.get("description"),
            "source": item.get("url"),
            "url": item.get("url"),
            "date": item.get("datePublished")
        })
    return results