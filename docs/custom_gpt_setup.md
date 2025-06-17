# Setup Guide: Health Records Copilot Custom GPT

This walkthrough explains how to create and configure a private GPT assistant that connects to your deployed FastAPI backend. Follow these steps in the OpenAI UI.

---

## 1. Create the GPT
1. Go to <https://platform.openai.com/gpts> and select **Create New GPT**.
2. Enter the basic configuration:
   - **Title**: `Health Records Copilot`
   - **Description**: `A private GPT assistant that helps users understand and summarize their health data from multiple portals.`
   - **Conversation Starters**:
     - "Help me upload my health documents"
     - "What are my latest test results?"
     - "Summarize my visit notes"
     - "Export my records"

## 2. System Instructions
Paste the following into the **Instructions** field:

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

## 3. Add API Actions
1. In the **Actions** tab choose **Create New Action**.
2. Provide your FastAPI OpenAPI schema URL:

```
https://<your-subdomain>.up.railway.app/openapi.json
```

3. Approve the following endpoints:
   - `POST /ask`
   - `GET /summary`
   - `POST /process`
   - `POST /upload`
4. Save the action and enable it.

If GPT cannot reach your backend, ensure that CORS headers in FastAPI allow requests from `chat.openai.com`.

## 4. Test the Assistant
- Start a chat and use a conversation starter, e.g. **"Help me upload my health documents"**.
- Upload a sample PDF or HTML file when prompted.
- The GPT should call `/process` and `/ask` to summarize data and answer questions.
- Verify that `/summary` returns structured results you can download.

---

## ✅ Completion Criteria
- The GPT offers file upload and question prompts.
- API calls execute successfully and display responses in chat.
- Answers from `/ask` reflect real data from the current session.
