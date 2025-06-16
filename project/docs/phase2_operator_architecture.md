# 📐 Architecture: Phase 2 – Operator-Assisted Health Data Collection

## 🎯 Goal
Empower users to retrieve health data from any portal with human-in-the-loop assistance via OpenAI Operator, guided entirely by ChatGPT Copilot. Users start, navigate, and return through the Copilot chat interface, while Operator handles portal interaction.

## 🧱 System Overview

### 👤 Unified User Workflow
1. **User starts in ChatGPT Copilot** and indicates they want to gather data.
2. **Copilot provides a button/link** to open OpenAI Operator with a pre-filled prompt.
3. **Operator launches**, opens health portal in browser.
4. **At login screen, user takes over manually** to authenticate.
5. **User gives Operator a search directive** (e.g., "download lab results").
6. **Operator locates the data**, confirms with user, and downloads file(s).
7. **Operator prompts user to return to Copilot** when done.
8. **Copilot gives the user a secure upload link** to a web form.
9. **User uploads files via form**, stored securely in Azure Blob.
10. **Copilot prompts user to confirm**, then runs ETL pipeline.
11. **User can ask questions or export their data** via `/ask`, `/export`, `/status`.

### 🔀 Data Flow
```
ChatGPT Copilot → Operator ⤴
  ↳ Portal interaction → Local download
User uploads via Web UI → Azure Blob
Copilot → ETL → Azure SQL
                     ↓
             /ask | /export | /status
```

## 🔐 Security & Consent
- **Upload UI uses SAS tokens**, scoped per session
- **Files are stored raw** (PDF, HTML), not read by GPT
- **User consent prompt before ETL**
- **Blobs auto-expire** after 24–72 hours

## 📦 Storage Choices
- **Azure Blob**: Secure upload and temporary holding area
- **Azure SQL**: Structured DB for all records

## 🔁 Handoff UX
- Copilot gives prompts to launch and return from Operator
- Uploads and analysis stay anchored in the Copilot chat

## 🧠 Benefits
- Secure, user-friendly, and scalable
- Avoids brittle scraping logic
- Keeps all health data handling within trust boundaries