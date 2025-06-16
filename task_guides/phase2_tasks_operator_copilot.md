# 📋 Phase 2 Task List – Operator + Copilot Integration

## 🧹 Overview
This task set supports replacing local scrapers with OpenAI Operator, while maintaining user flow through ChatGPT Copilot. It includes UX design for file handoff, secure storage, data shaping, and Copilot insight tools.

---

### 🧪 Task 201: Azure Blob Upload from User Device
- Design secure, user-friendly flow to upload files from local to Azure Blob
- MVP: Copilot provides upload link after user completes Operator session
- Backend validates file, stores in per-user/session Blob container
- Show upload success/failure feedback

### ↻ Task 202: Copilot ↔ Operator Prompt & UX
- Copilot provides prompt + instructions to launch Operator
- Pre-fill portal-specific prompts (labs, billing, visits)
- Instruct user to return to Copilot when done and upload the files
- Consider prompt template standard: "log in, download PDF of visit summary, save locally, return to Copilot"

### 📆 Task 203: ETL Ingestion from Blob
- Detect uploaded files from Azure Blob
- Run ETL against those files: extract → clean → structure
- Record metadata (upload timestamp, portal name, file type)

### 🔐 Task 204: Consent & Confirm Flow
- Prompt user before running ETL: “Ready to process the files you just uploaded?”
- Log consent event
- Add dry-run CLI override for dev/testing

### 📊 Task 205: View My Data (/status route)
- New `/status` tool that returns:
  - Which portals data has been loaded from
  - When they were last updated
  - What kinds of records are available (labs, visits, structured)
- Enable users to audit their data and decide if refresh is needed

### 🧰 Task 206: Storage Cleanup & Retention
- Set expiration on Azure blobs (e.g. 72hr TTL)
- Optional delete-after-ETL flag
- Add CLI/route to list or purge uploaded files

### 🧉 Task 207: Shape Operator Instructions Strategically
- Align Operator prompts with ETL targets:
  - Labs → PDF or HTML with test name, value, date
  - Visits → summaries with doctor, notes, provider
  - Billing → include amount, due date, type
- Include instruction to include filename, date, portal source
- Helps downstream structuring, audit, and reprocessing

---

## 🔗 Dependencies
- Azure Blob configured with secure uploads
- OpenAI Operator accessible to users
- ChatGPT Copilot via MCP or plugin (see note)

## 🔍 Open Questions
- ✅ Can ChatGPT (MCP) support these file upload/download/trigger interactions? 
- 🔄 Use `/status` route instead of full UI vault for now

## ⚡️ Build Mode (All Today)
- Parallel: Tasks 201, 202, 205, 207 (UX, Operator prompt, status route, strategic shaping)
- Serial: Task 201 must precede 203
- Parallel: Tasks 204 and 206 can be independent

## 📁 Example Task Files: to be committed under `task_guides/phase2_*`
- Each task follows standard format with Goal, Instructions, Files, Tests, Output checklist

This phase enables secure, guided, and extensible health data collection without code scrapers.