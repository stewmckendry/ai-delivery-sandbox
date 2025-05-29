## 🧱 Chunking Strategy for Large Artifact Payloads
### 🎯 Objective
Enable `generate_artifact_chain` to return full document content to GPT, even when its size exceeds the model's token limits, by splitting content into manageable, sequential chunks.

---

### ✅ Requirements
- **Support full artifact generation** without truncation.
- **Fit within GPT model limits** (~16k or 32k tokens, depending on context window).
- **Enable GPT to retrieve** and reconstruct full content over multiple turns.
- **Be stateless** on GPT's end—logic lives in backend.
- **Temporary storage** (e.g., in-memory store like Redis).

---

### 🔧 Design
- Run `generate_artifact_chain` as usual.
- Measure total token size of response.
- If over `MAX_TOKENS` (e.g., 12,000):
    - Split response into chunks (`PER_CHUNK_TOKENS`, e.g., 3,500).
    - Store in Redis with `session_id`-based keys.
    - Return first chunk + metadata: `is_chunked: True`, `chunk_index: 0`.
- GPT then calls `load_chunks(session_id)` to fetch more.

---

### 🛠️ Implementation

#### Constants
```python
MAX_TOKENS = 12000
PER_CHUNK_TOKENS = 3500
```

#### store_chunks
```python
def store_chunks(session_id, chunks, ttl=3600):
        for idx, chunk in enumerate(chunks):
                key = f"artifact_chunks:{session_id}:{idx}"
                redis_client.set(key, json.dumps(chunk), ex=ttl)
        redis_client.set(f"artifact_chunks:{session_id}:count", len(chunks), ex=ttl)
```

#### load_chunks
```python
def load_chunks(session_id):
        total_chunks = int(redis_client.get(f"artifact_chunks:{session_id}:count"))
        chunks = []
        for idx in range(total_chunks):
                key = f"artifact_chunks:{session_id}:{idx}"
                chunks.append(json.loads(redis_client.get(key)))
        return chunks
```

---

### 🧠 Interaction Flow
1. **User** clicks "Auto-Pilot" → GPT calls `generate_artifact_chain`.
2. **generate_artifact_chain** runs and checks token size.
3. **If > MAX_TOKENS:**
        - Split & store chunks.
        - Return first chunk + `is_chunked: True`, `chunk_index: 0`.
4. **GPT** detects `is_chunked` and calls helper tool `loadArtifactChunks(session_id)`.
5. **GPT** uses chunks for downstream actions (e.g., draft review).

---

### 🧪 Conditional Use in generate_artifact_chain
```python
if num_tokens(dump_result) > MAX_TOKENS:
        chunks = split_into_chunks(dump_result, PER_CHUNK_TOKENS)
        store_chunks(session_id, chunks)
        return {"chunked_result": chunks[0], "is_chunked": True, "chunk_index": 0}
else:
        return dump_result
```

---

### 📏 Token Threshold Rationale
- `MAX_TOKENS = 12000` ensures response + prompts stay under 16k limit.
- `PER_CHUNK_TOKENS = 3500` ensures safe fit with context window + metadata.

---

### 🔄 Future Design: LangChain Agent Orchestration
- An external LangChain agent could:
    - Page through chunk results.
    - Accumulate content in memory.
    - Manage summary-on-the-fly or query patterns.
- **Pros:** Dynamic reasoning across chunks.
- **Cons:** Increased infra complexity.

---

### 📍 Location
Committed to: `project/build/wps/WP27/chunking_strategy.md`

---

### ➕ Addendum: Chunking Design

#### What it does:
- For each section (`ArtifactSection`) individually:
    - Encodes its text using the tokenizer.
    - Breaks the tokenized text into multiple chunks if it exceeds `max_token`.
    - Decodes each chunk and adds it to the chunks list.
    - Each chunk is tied to a single `section_id` and labeled like `section-1-chunk1`, `section-1-chunk2`, etc.

#### What it doesn't do:
- Does **not** merge multiple sections together in a single chunk, even if some are small.
- Once section 1 is fully chunked, it proceeds to section 2, starting a new token count.

#### Implication:
- Keeps section boundaries intact, which is preferred for clarity and traceability when presenting or reviewing content.

#### tl;dr:
- If the entire document exceeds `max_tokens` (e.g., 12,000), it's split by section.
- If a single section exceeds the chunk size (e.g., 3,000), it's split into sub-chunks like `section_id-chunk1`, `section_id-chunk2`, etc.

**This structure:**
- Preserves the semantic boundaries of each section.
- Makes it easier for GPT to reason about, because each chunk retains full context of the section it belongs to.
- Is also easier for users to track and review, since chunks follow section structure logically.