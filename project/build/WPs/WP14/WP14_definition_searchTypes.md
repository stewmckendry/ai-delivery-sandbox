# 🧠 WP14 Design Note – Supporting Diverse External Search Types

## 🎯 Goal
Enable the `web_search` tool to support multiple specialized search types such as:
- General web
- StatsCan / public datasets
- Jurisdiction scans
- Market scans
- Academic research

These inform `generate_section` and other artifact workflows.

---

## 🧠 Strategy: Unified Interface with Internal Specialization

### 1. `web_search.py` as Main Entry
- Accepts a `search_type` parameter
- Routes to specialized handler modules internally
- Returns standardized output schema

### 2. Internal Handler Routing
```python
search_handlers = {
    "general": run_general_search,
    "statcan": run_statcan_query,
    "jurisdiction": run_jurisdiction_scan,
    "market": run_market_scan,
    "academic": run_academic_lookup,
}
```

### 3. Prompt Templates
Each handler uses a tailored prompt template:
```yaml
PROMPT_MARKET_SCAN: >
  Conduct a short market scan for the {artifact}.
  Focus on recent investments and public-private partnerships.

PROMPT_JURISDICTION_SCAN: >
  Scan major provinces or cities for pilots related to the {section} of a {artifact}.
```

---

## 📤 Standard Output Schema
Each search handler returns:
```json
{
  "summary": "Short human-readable result",
  "sources": ["https://..."],
  "raw_hits": [...]  // Optional structured source data
}
```

---

## 📁 Suggested File Structure
| File | Role |
|------|------|
| `web_search.py` | Main entry point and router |
| `search_handlers/general.py` | Google or DuckDuckGo scraping or API |
| `search_handlers/statcan.py` | StatsCan API or static dataset access |
| `search_handlers/academic.py` | Semantic Scholar, CORE, or OpenAlex |
| `prompts/search_prompts.yaml` | Prompt templates by search type |

---

## ✅ Integration Guidance
- Log `search_type` in `PromptLog` and `ReasoningTrace`
- Return formatted string or list to be added as `external_evidence`
- Support no-hit/fallback behavior gracefully
- Keep logic modular and composable for future extensions

---

## 🧠 Lessons to Apply
- Match output format expectations in downstream toolchain
- Keep prompt scaffolding lean and reusable
- Allow field-level metadata like `artifact`, `section`, `intent` to drive routing