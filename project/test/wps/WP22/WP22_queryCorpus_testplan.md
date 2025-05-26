# 🧪 WP22 Test Plan – queryCorpus

## 🎯 Goal
Verify that the `queryCorpus` tool retrieves relevant content from the embedded Open Government Guidebook corpus.

## 📘 Context
- Document: *Open Government Guidebook 2023*
- Embedded: via `loadCorpus.py`
- Chroma: using local instance (`./local_vector_store`)

## 🧪 Test Inputs
| Test | Query | Expectation |
|------|-------|-------------|
| T1 | "open government policy objectives" | Returns a summary referencing principles or goals |
| T2 | "digital services and transparency" | Mentions modernization or digital strategy links |
| T3 | "Canada's open data strategy" | References to datasets, portals, or initiatives |

## ✅ Success Criteria
- Result includes an `answer` or `results` key
- Output is non-empty and semantically matches the query intent

## 🧰 Tools
- `queryCorpus.py`
- OpenAI API key
- Local vector DB with loaded document

## ⏭ Follow-up
- Add new tests as more documents are embedded
- Compare against `goc_alignment_search` outputs once integrated