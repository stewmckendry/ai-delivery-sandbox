# Deploy Guide: `loadCorpus` and Vector Store Setup

## 1. 🧠 Vector Store Engine
- **Default (Dev)**: FAISS (local, fast, open-source)
- **Cloud Option**: Chroma + Docker + Volume Mount or Postgres

## 2. 📦 Setup Instructions (FAISS, Dev Mode)
```bash
pip install faiss-cpu numpy openai
```

## 3. 🌐 Setup Instructions (Chroma, Cloud Mode)
```bash
pip install chromadb
```

### Option A – Local Docker (for Railway or Azure container app)
- Use a `docker-compose.yaml` to mount persistent volume
- Example:
```yaml
services:
  chroma:
    image: chromadb/chroma
    ports:
      - "8000:8000"
    volumes:
      - ./data/chroma:/chroma/chroma
```

### Option B – Remote DB (Chroma + Postgres)
- Set `.env`:
```env
CHROMA_SERVER_HOST=https://your-deployed-url
CHROMA_SERVER_HTTP_PORT=8000
```
- Use `Settings` in `loadCorpus` to connect with API client

## 4. 🔐 Authorization (Embedding)
```env
OPENAI_API_KEY=sk-...
```

## 5. 📁 Directory Layout (Dev Mode)
- Vector index files: `data/vector_store/index.faiss`
- Metadata: `data/vector_store/index.json`

## 6. 🔄 Refresh Strategy
- Index updated on each `loadCorpus` call
- Remote stores push on add/update

## 7. 🔎 Retrieval Integration
- Planner tools will query based on metadata tags
- Match section, intent, gate, etc.

## 8. 🧪 Verification
```bash
python app/tools/tool_wrappers/loadCorpus.py --test
```
Expected:
- FAISS or Chroma index update
- Log in PromptLog
- Embedding count returned

---
✅ Guide supports dev and cloud. Use .env to switch configs.