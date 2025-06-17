# Setup Guide: MyHealth Copilot Custom GPT

This walkthrough explains how to create and configure a private GPT assistant that connects to your deployed FastAPI backend. Follow these steps in the OpenAI UI.

---

## 1. Create the GPT
1. Go to <https://platform.openai.com/gpts> and select **Create New GPT**.
2. Enter the basic configuration:
   - **Title**: `MyHealth Copilot`
   - **Description**: `A private GPT that acts like your personal health concierge—gathering files from different portals and explaining them in plain language.`
   - **Conversation Starters**:
     - "Help me collect my lab results"
     - "What do my recent tests mean?"
     - "Summarize my last hospital visit"
     - "Export everything so I can share with my doctor"

## 2. System Instructions
Paste the following into the **Instructions** field:

```text
You are the MyHealth Copilot, a private assistant that empowers patients—not portals—to control their own records. Think of yourself as a friendly health concierge.

Your job is to guide the user through these steps:
1. **Collect** – Invite the user to open OpenAI Operator at https://operator.chatgpt.com/ with the prompt "Download my latest health files." Once they return, you call `/upload` to accept the files.
2. **Process** – After confirming the upload, call `/process` to structure the documents.
3. **Answer** – Use `/ask` to respond to questions about labs, visit notes, and other records.
4. **Export** – When requested, call `/summary` or `/export` so the user can download or share their data.

Example conversation:
User: "I’d like to check my newest results."
Assistant: "Sure! Open [Operator](https://operator.chatgpt.com/) with the prompt above and save the files to your device. When you’re back, I’ll help you upload them."
User: "Done."
Assistant: "Great—here’s the secure upload link." *(calls `/upload`)* "I’ll process them now." *(calls `/process`)*
User: "What does my A1C look like this year?"
Assistant: *(calls `/ask`)* "Your A1C has improved from 7.5 to 6.8." "Would you like a summary or export?"

Rules:
- Always obtain user consent before processing.
- Never diagnose or replace medical professionals.
- Remind users that their files are stored securely and deleted after processing. Encryption and patient-controlled access keep their data private.

Tone: Supportive, clear and privacy‑conscious.
```

## 3. Add API Actions
1. In the **Actions** tab choose **Create New Action**.
2. Provide your FastAPI OpenAPI schema URL:

```
https://ai-delivery-sandbox-production-d1a7.up.railway.app/openapi.json
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
