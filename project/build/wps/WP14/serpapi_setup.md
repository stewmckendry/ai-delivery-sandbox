# SerpAPI Setup Guide for WP14

This guide walks through configuring SerpAPI for use in the PolicyGPT external search tool.

---

## 🛠️ Step-by-Step Setup

### 1. Create a SerpAPI Account
- Visit [https://serpapi.com/](https://serpapi.com/)
- Click **Sign Up** (free tier available)
- Verify your email and log in

### 2. Get Your API Key
- Go to your [account dashboard](https://serpapi.com/dashboard)
- Copy the **API Key** visible under your account info

### 3. Add the API Key to Your Environment

#### a. Locally
Update your `.env` file in the root project directory:
```env
SERPAPI_KEY=your_key_here
```

#### b. On Railway
- Go to your Railway project
- Open **Variables** tab
- Add new variable:
  - **Key:** `SERPAPI_KEY`
  - **Value:** your copied key

---

## 📋 Notes
- No billing required for small projects (free tier = 100 searches/month)
- We use Google search engine (default) via `engine=google`
- Supports filtering by date, site, domain, etc.

---

Once the key is set, your toolchain can call SerpAPI in `search_api_utils.py` using:
```python
url = "https://serpapi.com/search"
params = {
  "q": query,
  "api_key": os.getenv("SERPAPI_KEY"),
  "engine": "google",
  "num": 5
}
```