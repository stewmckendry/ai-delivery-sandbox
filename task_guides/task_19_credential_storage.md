# Codex Agent Task: Secure Credential Storage in Redis

## 🎯 Goal
Securely store and expire user-submitted credentials for scraping.

## 📂 Target File
- `app/storage/credentials.py`

## 📋 Instructions
- Create functions:
  - `store_credentials(portal: str, username: str, password: str)`
    - Encrypt password using Fernet key from env
    - Store all fields in Redis with TTL (10 minutes)
  - `get_credentials(portal: str)`
    - Decrypt and return stored values
  - `delete_credentials(portal: str)`
    - Clear from Redis manually or after use

## 🔄 Reuse
- `app/storage/redis.py` for Redis client

## 🧪 Test
- Create `tests/test_credentials.py`
- Verify encrypt/decrypt roundtrip
- Confirm TTL expiry logic

## ✅ What to Report Back
- Secure storage module
- Unit tests
- Example printout or retrieval log

Refer to `AGENTS.md` and `review_checklist.md` for structure.