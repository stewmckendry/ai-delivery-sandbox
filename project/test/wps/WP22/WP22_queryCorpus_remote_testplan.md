# 🌐 WP22 Test Plan – queryCorpus (Remote Mode)

## 🎯 Goal
Ensure the `queryCorpus.py` tool returns GPT-synthesized answers when connected to a remote Chroma vector DB instance (e.g., hosted on Railway).

## 🧪 Precondition
- Remote vector DB (e.g., Railway) must contain the *Open Government Guidebook 2023*.
- `CHROMA_SERVER_HOST` and `CHROMA_SERVER_HTTP_PORT` must be set in environment.
- `OPENAI_API_KEY` must be configured.

## 📘 Test Inputs
| Test | Query | Expectation |
|------|-------|-------------|
| R1 | "open government policy objectives" | Synthesized answer from top-matching remote chunks |
| R2 | "transparency and digital services" | Synthesized content related to digital strategies |

## ✅ Success Criteria
- Tool returns an `answer` key, not just `results`
- `answer` is coherent and contextually aligned with the query intent

## 📦 Artifacts
- `queryCorpus.py` (patched for remote synthesis)
- `loadCorpus.py` (to seed remote vector DB if needed)