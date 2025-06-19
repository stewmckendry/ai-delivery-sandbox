# 🤖 Task 315: Add Vector-Based RAG Support with Chroma

## 🎯 Goal
Implement a semantic retrieval pipeline to power `/ask` using ChromaDB. This will allow GPT to answer health questions based on semantic similarity to structured health records.

---

## 🧠 Why
- Current `/ask` is limited to top-N records and token truncation
- Doesn’t semantically rank relevance (e.g. "low iron" ↔ ferritin)
- Structured records cover a wide range of content, but are treated flatly

---

## ✅ What to Implement

### 1. **Chroma Vector Store Integration**
- Add `rag/indexer.py`:
  - Ingest structured records into Chroma per session_key
  - Chunk and embed using OpenAI or InstructorEmbeddings
  - Store metadata (type, code, date, abnormal flag, etc.)

- Add `rag/searcher.py`:
  - Semantic search top-N records by session + query
  - Filter by session_key to isolate user data
  - Return records for prompt context

### 2. **Enhance `/ask` to Use Vector Search**
- Update or create `/ask_vector` route in `app/api/rag.py`
  - Embed incoming query
  - Search Chroma
  - Assemble top-k results into GPT prompt
  - Return GPT answer

- Fallback to existing logic if Chroma not reachable

### 3. **Chroma Infrastructure (Railway)**
- Use attached Dockerfile + docker-compose.yaml to deploy Chroma to **separate Railway instance**
- Expose environment variables:
  ```env
  CHROMA_SERVER_HOST=your-chroma-url
  CHROMA_SERVER_HTTP_PORT=8000
  CHROMA_TOKEN=your_token
  USE_REMOTE_CHROMA=true
  ```

- Confirm FastAPI app connects using `HttpClient` (as in `queryCorpus.py`)

### 4. **Schema & Safety**
- Enforce session_key filters in Chroma queries
- Do not embed PHI-rich raw text — use only structured/summarized blocks
- Use short-lived tokens or scoped collections for session-bound access

---

## 🧪 Test Plan
- Upload real health records
- Index to Chroma
- Run `/ask_vector` with semantically phrased prompts:
  - "Do I have iron deficiency?"
  - "What were my ER visits for?"
- Validate GPT uses context returned from vector search

---

## ✅ Done When
- Chroma receives records per session and query
- GPT answers use semantically matched records
- `/ask` accuracy improves across broad question types

---

## 🔒 Security Note
- Session-scoped index access must be enforced
- Chroma must not expose multi-user data across sessions

---

Let Stewart know once indexing + search is live so he can test multiple session flows.