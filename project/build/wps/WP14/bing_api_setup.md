## Setting Up Bing Web Search API for WP14

This guide walks you through registering for a Bing Web Search API key and configuring your environment.

### Step 1: Register on Azure Marketplace
1. Visit [https://portal.azure.com](https://portal.azure.com)
2. Log in or create a Microsoft account.
3. In the portal, search for "Bing Search v7" or go directly to: [https://portal.azure.com/#create/Microsoft.CognitiveServicesBingSearch-v7](https://portal.azure.com/#create/Microsoft.CognitiveServicesBingSearch-v7)
4. Click **Create** and follow the steps:
   - Choose your subscription
   - Create a resource group or use an existing one
   - Set the pricing tier (Free available with 3K requests/month)
   - Create the resource

### Step 2: Get Your API Key
1. After creation, navigate to the new Bing Search resource.
2. Under the **Keys and Endpoint** section, copy one of the available keys.
3. Note the endpoint URL (typically `https://api.bing.microsoft.com/v7.0/search`)

### Step 3: Configure Your Environment
Create or update your local `.env` file:

```env
BING_API_KEY=your_copied_key_here
```

This will be used by WP14's `general.py` handler to perform real-time web search via Bing.

### Step 4 (Optional): Test Your Key
You can run a quick test using curl or Python:

```bash
curl -H "Ocp-Apim-Subscription-Key: $BING_API_KEY" \
     "https://api.bing.microsoft.com/v7.0/search?q=infrastructure+funding"
```

---

For development, make sure `BING_API_KEY` is loaded in your environment. If using VSCode or running via script, the `dotenv` loader will pick it up.

> Note: Free tier is sufficient for WP14 testing.

---

If you're using RapidAPI instead of Azure:
- Search for "Bing Web Search" on [https://rapidapi.com](https://rapidapi.com)
- Subscribe and follow similar steps to get a key and update the API call endpoint.