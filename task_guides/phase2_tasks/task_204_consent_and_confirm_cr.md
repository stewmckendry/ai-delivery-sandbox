# CR: Migrate Consent Step to Copilot Chat Flow

## 🔁 Context
Currently, Task 204 displays a standalone HTML form at `/process` to request user confirmation before running the ETL pipeline. This works technically but breaks the ChatGPT-first user experience.

## ❌ Problem
- User leaves Copilot to view and interact with `/process`
- It’s unclear how they return to the chat
- Experience feels disconnected from the Operator → Upload → Ask flow

## ✅ Proposed Change
- Move consent prompt and confirmation into ChatGPT Copilot
- User is prompted via `/status` if unprocessed uploads are found:
  > "You've uploaded 2 files. Would you like to analyze them now?"
  - If yes → trigger `/process` via internal API call (not UI)

## ✏️ Implementation Notes
- Remove `/process` HTML view
- Replace with `/status` suggestion + consent POST
- Log `consent_given` using `audit.log_event()` as before
- Use GPT chat prompt + tool invocation to simplify UX

## 📌 Notes
This CR improves alignment with our vision of a seamless, in-chat Copilot experience where the user never needs to leave the chat to confirm, upload, analyze, or query their health data.