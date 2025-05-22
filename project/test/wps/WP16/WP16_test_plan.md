# WP16 – Final Test Plan

This test plan validates all tools built or modified in WP16 in a Railway-deployed environment.

## 🧪 Prerequisites
- `.env` file or Railway variables set with:
  ```env
  OPENAI_API_KEY=sk-xxx
  CHROMA_SERVER_HOST=https://<your-chroma-url>
  CHROMA_SERVER_HTTP_PORT=8000
  ```
- App deployed and accessible at `https://<your-app>.up.railway.app`
- Local or Postman access for testing FastAPI endpoints

---

## ✅ Test 1 – `uploadTextInput`
**Tool:** `uploadTextInput`
```json
POST /tools/uploadTextInput
{
  "text": "Our department faces recurring delays due to legacy systems.",
  "metadata": {
    "gate": 0,
    "artifact": "investment_proposal_concept",
    "section": "problem_statement",
    "intent": "Describe the problem or opportunity."
  }
}
```
✅ **Expect:** `status: success`, PromptLog entry created

---

## ✅ Test 2 – `uploadFileInput`
**Tool:** `uploadFileInput`
```json
POST /tools/uploadFileInput
{
  "file_content": "Strategic alignment summary: Project aligns with 2024 innovation mandate.",
  "metadata": {
    "gate": 0,
    "artifact": "investment_proposal_concept",
    "section": "strategic_alignment",
    "intent": "Explain alignment with GoC priorities."
  }
}
```
✅ **Expect:** `status: success`, PromptLog entry created

---

## ✅ Test 3 – `uploadLinkInput`
**Tool:** `uploadLinkInput`
```json
POST /tools/uploadLinkInput
{
  "url": "https://example.com/example-project-page",
  "metadata": {
    "gate": 0,
    "artifact": "investment_proposal_concept",
    "section": "background",
    "intent": "Provide strategic background."
  }
}
```
✅ **Expect:** Web content scraped, logged, and trace path returned

---

## ✅ Test 4 – `loadCorpus`
**Tool:** `loadCorpus`
```json
POST /tools/loadCorpus
{
  "file_contents": "This document provides baseline risk and cost data for evaluation.",
  "file_name": "baseline_costs.docx",
  "metadata": {
    "gate": 1,
    "artifact": "business_case",
    "section": "cost_estimate",
    "intent": "Provide a cost estimate for the recommended option."
  }
}
```
✅ **Expect:** Embeddings generated, document indexed, PromptLog and Chroma updated

---

## ✅ Test 5 – `inputPromptGenerator`
**Tool:** `inputPromptGenerator`
```json
POST /tools/inputPromptGenerator
{
  "gate_id": 0,
  "artifact_id": "investment_proposal_concept"
}
```
✅ **Expect:** JSON array of prompts with metadata, section, hints, and maturity tags

---

## ✅ Test 6 – `inputChecker`
**Tool:** `inputChecker`
```json
POST /tools/inputChecker
{
  "session_id": "<same-session-used-in-above-tests>",
  "gate_id": 0,
  "artifact_id": "investment_proposal_concept"
}
```
✅ **Expect:** JSON list of missing intents by section

---

## 📎 Notes
- Include `Authorization` if required for API
- Use curl or Postman or browser-based tools
- Capture trace logs or snapshot output for review

---

## 🧪 Snapshot Export (Optional)
```bash
ls traces/snapshots/
cat traces/snapshots/<latest>.json
```
✅ Exported file should show `tool`, `input_summary`, `metadata`, and `output`
