# 🧠 Task 324: Improve Vector Prompt Quality for Small Record Sets

## 🧠 Context
The AI Health Records Assistant uses Chroma for semantic retrieval in `/ask_vector`. In cases where only 1–3 records are returned (such as in demo mode), GPT often fails to extract useful meaning.

The repo is `ai-delivery-sandbox`, branch `sandbox-curious-fox`.

## 📍 Issues Observed
- Chunks are often short (1–2 lines)
- Metadata like "Procedure" or "ER note" is not surfaced in GPT context
- Semantic distance between query and record (e.g., “ankle injury” vs “sprained ankle”) is not bridged by GPT

## ✅ Goal
Improve prompt quality in `/ask_vector` so that even small, sparse records still return meaningful GPT answers.

---

## 📦 What to Do

### 1. Improve Prompt Assembly in `rag.py`
Update the GPT prompt passed to include structured context per record:
```txt
Record 1:
Type: Procedure
Code: 6142004
Text: Patient treated for sprained ankle. Discharged with crutches.
```
Do this for every chunk returned by Chroma before inserting into the final GPT call.

### 2. Expand Metadata in Indexer
Update `index_structured_records` in `rag/indexer.py` to include additional fields:
- `display`
- `source_url`
- (Optional) source portal type: "ER", "lab", etc.

This will allow richer prompt framing and match what’s useful to GPT.

### 3. Add Richer Demo Content
As a fallback for minimal test data:
- Add 2–3 demo records per test PDF
- Use variant phrasing (e.g., “sprained ankle” vs “ankle injury”)
- Optionally add more descriptive sentences (e.g., “Seen at ER on March 10, discharged with crutches.”)

---

## 🧪 Done When
- GPT answers can accurately respond to demo questions like:
  - “Did I visit the ER?”
  - “What happened during my hospital visit?”
- Prompt fed to GPT includes both metadata and record text
- Small sessions return meaningful answers via `/ask_vector`

Let Stewart know when this is deployed so we can revalidate prompt outcomes with minimal records.