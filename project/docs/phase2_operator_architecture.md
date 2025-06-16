# 📊 Architecture: Phase 2 – Operator-Assisted Health Data Collection

## 🌟 Goal
Empower users to retrieve health data from any portal with human-in-the-loop assistance via OpenAI Operator, guided entirely by ChatGPT Copilot. Users start, navigate, and return through the Copilot chat interface, while Operator handles portal interaction.

## 🗺 System Overview

### 👤 Unified User Workflow
1. **User starts in ChatGPT Copilot** and indicates they want to gather data.
2. **Copilot provides a button/link** (or instructions) to open OpenAI Operator with a pre-filled prompt.
3. **Operator launches**, opens health portal in browser.
4. **At login screen, user takes over manually** to authenticate.
5. **User gives Operator a search directive** (e.g., "download lab results").
6. **Operator locates the data**, confirms with user, and downloads file(s).
7. **Files are stored in a secure Azure Blob folder**.
8. **Operator prompts user to return to Copilot** when done.
9. **User returns to Copilot**, says "done", and Copilot kicks off ETL.
10. **User can now ask questions or export their data** via `/ask` and `/export`.

### ↖️ Data Flow
```
ChatGPT Copilot → Operator ⤴
  ↳ Open Portal (User logs in)
  ↳ Download Health Files
  ↳ Store in Azure Blob
  ↳ Return to Copilot → ETL → Azure SQL
                                ↓
                           /ask | /export
```

## 🔐 Security & Consent
- **User-in-control at all steps**: no scraping, no stored credentials.
- **Consent checkpoints**: before download, before ETL.
- **Azure Blob**: stores files with time-limited, encrypted access.

## 📆 Storage Choices
- **Azure Blob**: Temporary file storage with per-user containers.
- **Azure SQL**: Destination for structured health data.
- Optional: Vault-style interface for managing files.

## ↺ Handoff UX
- **Copilot → Operator**: Copilot provides prompt/link to launch Operator.
- **Operator → Copilot**: Operator reminds user to return to Copilot when finished.

## 🧠 Benefits
- Seamless experience: users stay anchored in ChatGPT Copilot.
- Reduces burden of scraping logic and maintenance.
- Fully adaptable across portals and health systems.
- Prioritizes privacy, clarity, and flexibility for non-technical users.