# WP16 – Final Test Plan

This test plan validates all tools built or modified in WP16 in a Railway-deployed environment.

## 🧪 Prerequisites
- `.env` file or Railway variables set with:
  ```env
  OPENAI_API_KEY=sk-xxx
  CHROMA_SERVER_HOST=https://<your-chroma-url>
  CHROMA_SERVER_HTTP_PORT=8000
  ```
- App deployed and accessible at `https://robust-adventure-production.up.railway.app`
- Use `curl` or Postman to test FastAPI endpoints

---

## ✅ Test 1 – `uploadTextInput`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/uploadTextInput \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Our department faces recurring delays due to legacy systems.",
           "metadata": {
             "gate": 0,
             "artifact": "investment_proposal_concept",
             "section": "problem_statement",
             "intent": "Describe the problem or opportunity."
           }
         }'
```
✅ Expect: `status: success`, PromptLog entry created

---

## ✅ Test 2 – `uploadFileInput`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/uploadFileInput \
     -H "Content-Type: application/json" \
     -d '{
           "file_content": "Strategic alignment summary: Project aligns with 2024 innovation mandate.",
           "metadata": {
             "gate": 0,
             "artifact": "investment_proposal_concept",
             "section": "strategic_alignment",
             "intent": "Explain alignment with GoC priorities."
           }
         }'
```
✅ Expect: `status: success`, PromptLog entry created

---

## ✅ Test 3 – `uploadLinkInput`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/uploadLinkInput \
     -H "Content-Type: application/json" \
     -d '{
           "url": "https://example.com/example-project-page",
           "metadata": {
             "gate": 0,
             "artifact": "investment_proposal_concept",
             "section": "background",
             "intent": "Provide strategic background."
           }
         }'
```
✅ Expect: content scraped, trace path returned, PromptLog updated

---

## ✅ Test 4 – `loadCorpus`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/loadCorpus \
     -H "Content-Type: application/json" \
     -d '{
           "file_contents": "This document provides baseline risk and cost data for evaluation.",
           "file_name": "baseline_costs.docx",
           "metadata": {
             "gate": 1,
             "artifact": "business_case",
             "section": "cost_estimate",
             "intent": "Provide a cost estimate for the recommended option."
           }
         }'
```
✅ Expect: document indexed, vector store updated, PromptLog entry

---

## ✅ Test 5 – `inputPromptGenerator`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/inputPromptGenerator \
     -H "Content-Type: application/json" \
     -d '{
           "gate_id": 0,
           "artifact_id": "investment_proposal_concept"
         }'
```
✅ Expect: array of input prompts with metadata

---

## ✅ Test 6 – `inputChecker`
```bash
curl -X POST https://robust-adventure-production.up.railway.app/tools/inputChecker \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "<same-session-used-in-above-tests>",
           "gate_id": 0,
           "artifact_id": "investment_proposal_concept"
         }'
```
✅ Expect: JSON with missing intents by section

---

## 📎 Notes
- Replace `<same-session-used-in-above-tests>` with real session_id from PromptLog
- Optional: enable API logs or snapshot writing to verify trace content

---

## 🧪 Snapshot Export (Optional)
```bash
ls traces/snapshots/
cat traces/snapshots/<latest>.json
```
✅ Exported snapshot shows `tool`, `input_summary`, `metadata`, `output`
