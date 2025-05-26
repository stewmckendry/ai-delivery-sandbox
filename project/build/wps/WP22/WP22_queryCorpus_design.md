## 🧠 WP22 Tool Design – queryCorpus

### 📌 Purpose
The `queryCorpus` tool enables semantic search over an embedded policy document corpus (e.g., Open Government Guidebook). It's part of the WP22 toolchain for discovering alignment between draft text and Government of Canada strategies.

### 🛠 Key Functions
- Accepts a natural language query string.
- Connects to either a **local Chroma DB** or **remote instance** (e.g., Railway-hosted vector store).
- Retrieves and summarizes top-matching content using LangChain’s `RetrievalQA` (local) or direct collection query (remote).

### 🧩 Components
| Component | Role |
|-----------|------|
| `CHROMA_DIR` | Local Chroma directory for dev/test |
| `CHROMA_HOST`, `CHROMA_PORT` | Remote Chroma setup via env vars |
| `USE_REMOTE_CHROMA` | Boolean flag to route query mode |

### 🔁 Logic Flow
1. Validate input query
2. If `CHROMA_HOST` is set:
   - Use `HttpClient` to query the `policygpt` collection
3. Else:
   - Use LangChain to retrieve + synthesize answer via GPT
4. Return structured output

### ✅ Usage
- Can be called from planner directly
- Used as part of `goc_alignment_search.py`
- Enables testing of embedded policy corpus prior to full toolchain integration

---

### 📎 Output Explanation
- The tool returns either a GPT-synthesized **answer** (local mode) or raw **results** (remote mode).
- Each result reflects the most relevant "chunk" (section of the original document) matching the query.

### 📚 How Chunks Are Created
- Chunks are split using LangChain's `RecursiveCharacterTextSplitter`.
- Default chunk size is ~500 characters with 50 character overlap.
- This is arbitrary and not based on section headers or semantic segmentation.

### 🔁 How Embedding Works
- Each chunk is converted to a vector using `OpenAIEmbeddings()`.
- On Railway or cloud deployments, the same embedding model applies—provided the `OPENAI_API_KEY` is configured.
- This ensures query behavior is consistent across local and remote environments.