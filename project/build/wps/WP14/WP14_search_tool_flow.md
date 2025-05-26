## WP14 Search Tool Flow

This document summarizes the logic, handlers, and query formulation strategy for the `webSearch` tool.

---

### 🔁 Overall Flow
```
Planner (intent: external_web_search)
  → Tool: webSearch.run_tool()
    → Handler: based on `search_type`
      - general.py
      - jurisdiction.py
      - market.py
    → Query sent to Bing (via RapidAPI)
    → Results normalized and returned
    → Log written to WebSearchLog
```

---

### 🔍 Handler Strategies

#### `general`
- Passes `query` directly to Bing
- Uses:
  ```bash
  freshness=Day, safeSearch=Off
  ```
- Returns top N public web results (news, reports, etc.)

#### `jurisdiction`
- Appends location from context (e.g. `Canada digital identity`)
- Adds domain filter:
  ```bash
  site:.gov OR site:.gc.ca OR site:.gov.uk
  ```
- Useful for public sector policy scans

#### `market`
- Appends sector or industry from context (if available)
- Adds business relevance terms:
  ```bash
  vendors OR suppliers OR case study
  ```
- Targets commercial/industry content

---

### 🌐 Search Source
- **Provider:** Bing Web Search via RapidAPI
- **Endpoint:** `https://bing-web-search1.p.rapidapi.com/search`
- **Params used:**
  - `q`, `mkt`, `freshness`, `textFormat`, `count`
  - Headers: `X-RapidAPI-Key`, `X-RapidAPI-Host`

---

### 📄 Prompt Templates
Stored in: `project/prompts/search_prompts.yaml`
Used to shape tone and style for synthesis tools (if needed).

---

### 📦 Output Structure
```json
[
  {
    "title": "...",
    "snippet": "...",
    "source": "...",
    "date": "...",
    "url": "..."
  }
]
```

---

### 🧪 Extensibility
New `search_type` handlers can be added with:
- Handler in `search_handlers/<type>.py`
- Prompt entry in `search_prompts.yaml`
- Routing entry in `web_search.py`

Future types: `academic`, `case_law`, `gov_policy`, `regulatory`, etc.