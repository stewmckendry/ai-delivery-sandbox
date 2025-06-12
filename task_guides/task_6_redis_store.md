# Codex Agent Task: Redis Session Store Utility

## 🎯 Goal
Create a Redis-based utility module for storing session state.

## 📂 Target File
- `app/storage/redis.py`

## 📋 Instructions
- Use the `redis` library to connect to a Redis instance
- Load config from `.env`: REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
- Implement simple functions: `set_key`, `get_key`, `delete_key`
- Include a `__main__` block to demonstrate usage
- Optionally include `is_connected()` health check

## ✅ What to Report Back
- File path and code
- How to test manually
- Unit test file and test run output (e.g. pytest)
- Any assumptions or limitations (e.g. mock Redis for test)

Refer to `task_guides/review_checklist.md` for structure.