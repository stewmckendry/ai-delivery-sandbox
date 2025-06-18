# ✅ Task 304: End-to-End Testing with MyHealth Copilot GPT

## 🎯 Goal
Verify that the MyHealth Copilot Custom GPT assistant can guide users through upload, trigger ETL, and answer questions using the structured data from your deployed FastAPI API.

---

## 🤖 GPT Assistant
- Name: **MyHealth Copilot**
- Linked to: `https://ai-delivery-sandbox-production-d1a7.up.railway.app/openapi.json`

---

## 🧪 Test Flow
Each step includes a **sample prompt** to input into GPT.

### 1. Start Interaction
**Prompt:**
```
Hi, I want to understand my recent medical results.
```
- ✅ GPT should respond with guidance to upload a file and provide a secure upload link (via `/upload/sas`)

### 2. Upload Flow
- Obtain a session key from `/session`.
- Use the GPT-uploaded link or `/upload?session=<key>&portal=strava`
- Upload `.html` or `.pdf` file
- GPT should offer to process it next

### 3. Trigger ETL
**Prompt:**
```
Yes, go ahead and process the file I uploaded.
```
- ✅ GPT should call `/process` with the session key

### 4. Ask Questions
**Prompt:**
```
What are the results of my last lab tests?
```
- ✅ GPT should call `/ask` and respond with structured lab results

**Prompt:**
```
Summarize my recent doctor visit notes.
```
- ✅ GPT includes structured summaries if visit notes are present

### 5. Export Records
**Prompt:**
```
Export all my records as PDF.
```
- ✅ GPT should call `/export` with format=pdf and provide download link

---

## ✅ Done When
- GPT guides upload and correctly calls `/process`, `/ask`, and `/export`
- GPT responses reflect uploaded content
- All calls hit the live Railway-hosted FastAPI

Please report:
- Prompts used
- GPT responses and API outputs
- Any failures or missing steps
