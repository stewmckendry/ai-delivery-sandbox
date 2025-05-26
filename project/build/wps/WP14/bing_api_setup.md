## Setting Up Bing Web Search API for WP14 (via RapidAPI)

This guide walks you through using Bing Web Search with [RapidAPI](https://rapidapi.com), since Azure no longer supports new deployments.

### Step 1: Create a RapidAPI Account
1. Visit [https://rapidapi.com](https://rapidapi.com)
2. Create an account or log in

### Step 2: Subscribe to Bing Search API
1. Search for "Bing Web Search" or go to:
   [https://rapidapi.com/contextualwebsearch/api/web-search](https://rapidapi.com/contextualwebsearch/api/web-search)
2. Click **Subscribe to Test** (choose Free plan)
3. After subscribing, go to the **Endpoints** tab
4. Copy the `X-RapidAPI-Key`

### Step 3: Configure `.env`
Create or update your local `.env` file:

```env
BING_API_KEY=your_rapidapi_key_here
```

### Step 4: Verify API Works
```bash
curl --request GET \
  --url 'https://bing-web-search1.p.rapidapi.com/search?mkt=en-us&safeSearch=Off&textFormat=Raw&freshness=Day&q=test' \
  --header 'X-RapidAPI-Key: your_rapidapi_key_here' \
  --header 'X-RapidAPI-Host: bing-web-search1.p.rapidapi.com'
```

---

This enables real-time web search in WP14 across handlers: `general`, `jurisdiction`, `market`.

> Tip: Use the Free plan for development. Upgrade if more volume is needed.

Let the searching begin 🔍