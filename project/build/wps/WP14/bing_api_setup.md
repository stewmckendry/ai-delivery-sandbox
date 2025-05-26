## Setting Up Bing Web Search API for WP14

This guide walks you through registering for a Bing Web Search API key and configuring your environment.

### Step 1: Register on Microsoft Azure or Bing Search Services
1. Go to the [Bing Search API documentation](https://learn.microsoft.com/en-us/bing/search-apis/)
2. Follow the latest setup guidance under "Get Started" > "Bing Web Search"
3. Create or log in to a Microsoft Azure account
4. Register a **Bing Search v7** resource (under Cognitive Services or new Bing Services)
5. Choose pricing tier (Free tier includes 3K/month)

### Step 2: Get Your API Key
1. Navigate to your Bing resource in the Azure portal
2. Go to **Keys and Endpoint** section
3. Copy an API key and the endpoint URL (e.g. `https://api.bing.microsoft.com/v7.0/search`)

### Step 3: Configure Your Environment
Create or update your local `.env` file:

```env
BING_API_KEY=your_copied_key_here
```

This enables WP14’s real-time search handler to access Bing.

### Step 4 (Optional): Test Your Key
```bash
curl -H "Ocp-Apim-Subscription-Key: $BING_API_KEY" \
     "https://api.bing.microsoft.com/v7.0/search?q=example+policy"
```

---

For devs: If using dotenv, this key will load automatically.

> Tip: Use Free tier for development. Upgrade only if doing heavy usage or integration testing.

---

If using RapidAPI:
- Visit [https://rapidapi.com](https://rapidapi.com)
- Search for "Bing Web Search"
- Subscribe and use their endpoint + API key in the same `.env` variable