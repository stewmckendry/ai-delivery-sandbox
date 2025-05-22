# Deploy Guide: `loadCorpus` and Vector Store Setup

## 1. 🧠 Vector Store Engine
- **Default**: FAISS (local, fast, open-source)
- **Optional**: Pinecone or Weaviate (for cloud-scale)

## 2. 📦 Setup Instructions (FAISS)
- Install dependencies: `faiss-cpu` or `faiss-gpu`
- Ensure `faiss`, `numpy`, and `openai` libraries are installed:
  ```bash
  pip install faiss-cpu numpy openai
  ```

## 3. 🔐 Authorization (Embedding)
- Requires OpenAI API key
- Set in `.env`:
  ```env
  OPENAI_API_KEY=sk-...
  ```

## 4. 📁 Directory Layout
- Vector index files stored in: `data/vector_store/index.faiss`
- Metadata saved in: `data/vector_store/index.json`

## 5. 🔄 Refresh Strategy
- Vector index is updated on each `loadCorpus` call
- If using a persistent store (e.g., Pinecone), push embeddings remotely

## 6. 🔎 Retrieval Integration
- Other tools query this index using cosine similarity
- See: `compose_and_cite`, `review_and_reflect`

## 7. 🧪 Verification
Run a test:
```bash
python app/tools/tool_wrappers/loadCorpus.py --test
```

Expected output:
- Confirmation of FAISS index creation
- Log entry in PromptLog
- Retrieval success from test query

---

✅ This guide supports dev and cloud usage. Adjust based on scale and infra policies.