# Codex Agent Task: Scaffold FastAPI App (Railway-ready)

## 🎯 Goal
Create the base FastAPI app structure and health check endpoint.

## 📂 Target Files
- `app/main.py`
- `run_local.sh`
- (Empty) `app/api/__init__.py`

## 📋 Instructions
- Use FastAPI to create an app instance
- Define a root route (`/`) that returns `{ "status": "ok" }`
- Prepare to mount future routers from `app/api/`
- Add a `run_local.sh` that runs Uvicorn with hot reload
- Make sure it’s compatible with Railway (env PORT or default 8000)

## ✅ What to Report Back
- File paths and full content
- CLI commands to run locally
- Test output: request to `/` returns expected JSON
- Unit test included (if practical) + test result
- Any config needed for Railway deployment

Refer to `task_guides/review_checklist.md` for structure.