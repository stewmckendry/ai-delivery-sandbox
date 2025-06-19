# 🪵 Task 316: Add Detailed Logging to API Routes

## 🎯 Goal
Add richer and more granular `logger.info(...)` and `logger.error(...)` output to key API flows to improve debugging and traceability in Railway logs.

---

## 📍 Target API Endpoints

### 1. `/process` (in `run_etl_from_blob`)
- Log:
  - When files are loaded
  - When ETL starts and ends
  - Count of extracted records
  - Any classification or annotation failures

### 2. `/ask_vector`
- Log:
  - Incoming session_key and query
  - Whether Chroma search succeeded or failed
  - Count and types of records returned
  - Truncated preview of prompt and GPT response

### 3. `/summary`
- Log:
  - Incoming session_key
  - Number of uploads and records returned
  - Any missing/empty tables

### 4. `/export`
- Log:
  - Session and format requested
  - Count of records exported
  - Filename or Blob path generated

---

## ✅ Guidelines
- Use `logger.info(...)` for all major steps and counts
- Use `logger.error(...)` for any failed extractions, Chroma calls, or empty record warnings
- Include `session_key` in all logs for traceability
- Avoid logging full user content (e.g. entire `text`) unless debugging locally

---

## 🧪 Done When
- Logs for each API are visible in Railway or local runs
- You can trace the flow of `/process`, `/ask_vector`, `/summary`, `/export` from start to end by reading logs
- Logs help surface indexing errors, empty GPT prompts, or export file paths

Let Stewart know when committed so he can verify live behavior via Railway logs.