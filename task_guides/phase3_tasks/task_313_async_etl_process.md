# ⚙️ Task 313: Make `/process` Run ETL in Background

## 🎯 Goal
Ensure the `/process` endpoint returns immediately and runs ETL in the background to avoid timeout errors in GPT or client tools.

---

## 🔍 Problem
- ETL can take 30–90 seconds for large files (PDF/HTML)
- Current `/process` call is synchronous — blocks client and risks 504 timeout (especially in GPT or cloud tools)

---

## ✅ Fix Plan
1. Update `/process` in `app/api/etl.py` to use FastAPI’s `BackgroundTasks`:

```python
from fastapi import BackgroundTasks

@router.post("/process")
def run_process(session_key: str, bg: BackgroundTasks):
    bg.add_task(run_etl_from_blob, session_key)
    return { "status": "processing", "session_key": session_key }
```

2. ETL logic in `orchestrator.py` remains unchanged — it just runs after the response returns

3. Return a clear message:
```json
{
  "status": "processing",
  "message": "Your files are being processed. Please check /summary later.",
  "session_key": "abc123"
}
```

---

## 🧪 Test Plan
- Upload a real PDF/HTML
- Trigger `/process`
- Confirm:
  - Response returns in < 1 second
  - ETL runs in background (check logs)
  - Records appear later in `/summary`

---

## ✅ Done When
- `/process` no longer blocks during ETL
- Works safely with GPT calls
- Status message guides user to check `/summary` or `/status` later