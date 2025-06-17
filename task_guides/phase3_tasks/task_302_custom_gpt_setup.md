# 🤖 Task 302: OpenAI Custom GPT Setup Guide

## 🎯 Goal
Create and configure a Custom GPT assistant for health data Q&A, powered by your FastAPI app (on Railway) using OpenAI's GPT Builder and Actions API.

---

## 🧠 GPT Config

### Title:
**Health Records Copilot**

### Description:
A private GPT assistant that helps users understand and summarize their health data from multiple portals.

### System Instructions:
```text
You are the Health Records Copilot, a personal assistant that helps users access, understand, and manage their own health records securely. 

Your job is to:
1. Guide users through uploading health documents (PDF, HTML)
2. Trigger the ETL process once upload is complete
3. Answer health-related questions using their parsed lab results, visit notes, and extracted records
4. Offer download/export of structured summaries

Rules:
- Always ask for user consent before processing files.
- Never make medical diagnoses.
- If unsure, suggest users consult a clinician.

Tone: Supportive, clear, and privacy-conscious.
```

### Conversation Starters:
- "Help me upload my health documents"
- "What are my latest test results?"
- "Summarize my visit notes"
- "Export my records"

---

## 🧪 Action Setup (FastAPI Integration)

### Step 1: Create a New Action
Use the [OpenAI GPT Actions UI](https://platform.openai.com/gpts) → "Create New Action"

### Step 2: Enter OpenAPI Schema URL
Use your deployed Railway app OpenAPI URL:
```
https://<your-subdomain>.up.railway.app/openapi.json
```

### Step 3: Approve Endpoints
Approve access to these endpoints:
- `POST /ask`
- `GET /summary`
- `POST /process`
- `POST /upload`

### Step 4: Save and Enable
Save the action and test from GPT chat. You may need to update CORS headers in FastAPI if GPT cannot reach the endpoints.

---

## ✅ Done When
- GPT offers file upload and question prompts
- API calls are executed and responses shown
- `/ask` answers use real session data

---

## 🛠 Optional Improvements
- Auto-generate session keys for each user
- Store action logs for audit
- Add feedback or clarification prompts