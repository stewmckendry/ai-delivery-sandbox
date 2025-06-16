# 📋 Phase 2 Task List – Operator + Copilot Integration

## 🧩 Overview
This task set supports replacing local scrapers with OpenAI Operator, while maintaining user flow through ChatGPT Copilot. It includes storage setup, handoff UX, and ETL integration with the new source.

---

### 🧪 Task 201: Setup Azure Blob for Secure Upload
- Provision Blob Storage container per user/session
- Generate time-limited upload/download URLs
- Secure read/write credentials via env vars or managed identity
- Validate file access and isolation

### 🔁 Task 202: Copilot ↔ Operator Prompt & UX
- Design Copilot prompts:
  - Launch Operator with portal prompts
  - Remind user to return when done
- Operator prompt templates:
  - "Login to [portal], go to Labs, download as PDF"
  - "Store in secure health folder"

### 📦 Task 203: ETL Ingestion from Blob
- Add Blob ingestion mode to existing ETL pipeline
- Use Blob SDK to fetch user files
- Handle different formats: PDF, HTML, text
- Reuse existing extractors + summarizer

### 🔐 Task 204: Consent & Confirm Flow
- Add prompt to confirm before running ETL
- Log consent for audit trail
- Add CLI bypass option for dev/test

### 🧰 Task 205: Storage Cleanup & Retention
- Auto-expire blobs after 24-72 hours
- Add optional user-facing delete button or CLI
- Prevent re-processing of same file

### 📊 Task 206: Vault UI (Optional)
- MVP file browser for user (or admin)
- View + delete blobs by portal/date
- Add file metadata: source, portal, type

---

## 🔗 Dependencies
- Azure Blob storage access
- OpenAI Operator available to end users
- ChatGPT Copilot with MCP integration

## 📅 Phase Scope
- Label: `phase2_operator`
- Timeline: Week 1 = Storage + Prompting, Week 2 = ETL + UX, Week 3 = Polish

This enables secure, UX-friendly, and extensible health data loading for users across any portal.