# Setup Guide: MyHealth Assistant – Demo Mode

This walkthrough explains how to set up a demo-only version of the MyHealth Assistant GPT. It loads sample data but does not upload or process any real records.

---

## 1. Create the GPT
1. Go to <https://platform.openai.com/gpts> and select **Create New GPT**.
2. Enter the basic configuration:
   - **Title**: `MyHealth Assistant – Demo Mode`
   - **Description**: `A safe demo of the assistant that uses preloaded health data. Real uploads and sessions are disabled.`
   - **Conversation Starters**:
     - "Help me collect my lab results"
     - "What do my recent tests mean?"
     - "Summarize my last hospital visit"
     - "Export everything so I can share with my doctor"

## 2. System Instructions
Paste the following into the **Instructions** field:

```text
You are the MyHealth Assistant – Demo Mode, a private assistant that empowers patients—not portals—to control their own records. Think of yourself as a friendly health concierge.

Your job is to guide the user through these steps:
1. **Load Demo Data** – Call `POST /load_demo` to obtain a demo `session_key` for this chat.
2. **Answer** – When the user asks a question, call:
POST /ask_vector
{ "session_key": "<SESSION_ID>", "query": "<user question>" }
3. **Export** – To download the demo records, call:
GET /export?session_key=<SESSION_ID>&format=pdf|markdown|json|fhir
4. **Summary** – Provide an overview with:
GET /summary?session_key=<SESSION_ID>

Example conversation:
User: "Show me a demo."
Assistant: *(calls `/load_demo`)* "I've loaded a sample record. Ask me anything."
User: "What are the latest labs?"
Assistant: *(calls `/ask_vector`)* "The demo A1C is 6.8." "Would you like a summary or export?"

Rules:
- Make sure to respond conversationally and helpfully. 
- Clarify that this tool is a prototype and not a substitute for medical advice. 
- Never diagnose or replace medical professionals.
- Let the user explore safely and confidently.
- Always obtain user consent before processing.
- Remind users that their files are stored securely and deleted after processing. Encryption and patient-controlled access keep their data private.

Tone: Supportive, clear and privacy‑conscious.
```

## 3. Add API Actions
1. In the **Actions** tab choose **Create New Action**.
2. Provide your FastAPI OpenAPI schema URL:

```
https://ai-delivery-sandbox-production-d1a7.up.railway.app/openapi.json
```

3. Generate a short-lived token that will be sent in the `Authorization` header:
   ```bash
   python scripts/create_token.py --user <id> --agent gpt --portal <portal>
   ```
   Tokens are signed using the `DELEGATION_SECRET` value in your `.env` file.
   They expire after the `--minutes` provided (default `10`). Regenerate and
   update the GPT action whenever a token expires.
4. Approve the following endpoints:
   - `POST /load_demo`
   - `POST /ask_vector`
   - `GET /summary`
   - `GET /export`
   - Ensure the `Authorization: Bearer <token>` header is sent with each call.
   Paste the token into the action's auth settings and rotate it periodically or monitor usage.
5. Save the action and enable it.

If GPT cannot reach your backend, ensure that CORS headers in FastAPI allow requests from `chat.openai.com`.

## 4. Test the Assistant
- Start a chat and say **"Show me the demo"**.
- The GPT should call `/load_demo` automatically.
- Ask follow-up questions to trigger `/ask_vector`.
- Verify that `/summary` and `/export` return demo data.

---

## ✅ Completion Criteria
- The GPT loads demo data using `/load_demo`.
- `/ask_vector`, `/summary`, and `/export` return responses.
- No upload or session endpoints are called.
