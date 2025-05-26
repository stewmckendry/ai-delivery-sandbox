# 🧵 WP22 – Async Design for `loadCorpus`

## 🎯 Objective
Prevent timeouts and improve responsiveness for large corpus ingestion by making the `loadCorpus` tool asynchronous. This enables smooth operation in Railway and other cloud environments where execution time or memory may be limited.

---

## 🧠 Technical Design

### 1. **Tool Attribute for Async**
```python
class Tool:
    async_tool = True
```
- This flag signals the API router to run the tool as a background task using FastAPI’s `BackgroundTasks`.
- All other tools default to synchronous execution unless they explicitly set this flag.

### 2. **API Router Behavior**
In `api_router.py`, the logic:
```python
if getattr(tool, "async_tool", False):
    return tool.run_tool(input_data, background_tasks=background_tasks)
else:
    return tool.run_tool(input_data)
```
- Automatically detects and routes async-capable tools.
- No change to calling syntax or routes for users or GPTs.

### 3. **Async Execution Flow**
- Immediately returns a response:
```json
{ "status": "accepted", "job_id": "<uuid>" }
```
- Tool logic continues embedding in the background.
- Tool writes logs, saves trace, and persists vector store as usual.

---

## 🧪 Use Case

- Embedding large policy PDFs with OpenAI embeddings and Chroma DB takes 20–90s.
- On Railway, this often causes a `502: Application failed to respond`.
- Async solves this by releasing the request thread and continuing work.

---

## 🧩 Compatibility

- No changes needed for:
  - `queryCorpus`
  - Planner toolchains
  - Calling patterns by users or GPT

Optional enhancements (future):
- `/status/{job_id}` endpoint
- Logging progress or estimated time

✅ `loadCorpus` is now safe to use in cloud or high-latency environments.