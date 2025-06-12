# Task 27: Full Pipeline Test Harness + Execution Plan

## 🎯 Goal
Systematically test the full AI scraping pipeline across a progression of healthcare portals (mock and real), tracking outcomes, bugs, and improvements.

## 🧪 Test Strategy
| Stage | Portal Type | Goal |
|---|---|---|
| 1 | Fake portal (static HTML) | Validate traversal, extraction, chunking, JSON output |
| 2 | Real public portal (no login) | Check LLM parsing on real data layout |
| 3 | Portal with login (no MFA) | Validate secure credential handling, challenge bypass |
| 4 | Portal with MFA or CAPTCHA | Validate pause/resume loop and human input handling |

## 🔁 Harness Behavior
- Calls `run_etl_for_portal()`
- Logs:
  - Crawl links and visited pages
  - Extracted chunks and summaries
  - Metadata (type, date, source)
  - Time per stage
- Outputs:
  - Structured JSON
  - Screenshots for paused challenges (if any)
  - Audit log entry

## 📋 Output Log Example
```json
{
  "portal": "fake_site",
  "start_time": "...",
  "pages_scraped": 4,
  "chunks_extracted": 12,
  "summarization_steps": 3,
  "output_file": "structured_lab_summary.json"
}
```

## 🤝 Roles
| Role | What They Do |
|---|---|
| You (Human Lead) | Choose test portals, approve challenges, review outputs |
| Me (Pipeline Orchestrator) | Run flows, report summaries, propose next test |
| Codex Agent | Fix bugs, improve modules, implement enhancements |

## 🔄 Workflow
1. You trigger test (CLI or ChatGPT command)
2. I execute flow, log all artifacts, and post summary
3. You review output
4. Any issues → spun off as tickets to Codex
5. We close the loop with a passing run

---

## ✅ What to Build
- Add CLI script: `scripts/run_portal_test.py`
- Accept `--portal`, `--depth`, `--debug` args
- Log all outputs to `/logs/portal_runs/<portal>_<timestamp>.json`
- Output JSON and markdown preview