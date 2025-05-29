## ✅ WP27 Iteration 3 – Test Plan for End-to-End UX Validation

### 🎯 Objective
Validate that each toolchain and tool introduced or updated in Iteration 3 performs correctly both individually and as part of an end-to-end UX for policy artifact generation.

---

### 🧪 Test Cases

#### 1. **Ingest Input**
- Tool: `IngestInputChain`
- Inputs: Sample project text + metadata
- Expected: Profile saved, raw text returned, metadata persisted

#### 2. **Global Context Chain**
- Toolchain: `global_context_chain`
- Inputs: `project_id`, `session_id`, `artifact_id`
- Expected: Search query, corpus results, web summary, alignment hits, all logged

#### 3. **Manual Section Generation**
- Toolchain: `generate_section_chain`
- Inputs: Project profile, memory, global context
- Expected: Memory + prior sections summarized, draft created and saved

#### 4. **Artifact Auto-Generation**
- Toolchain: `generate_artifact_chain`
- Inputs: Full session metadata
- Expected: All sections generated, global context used, chunking invoked if tokens exceed limit

#### 5. **Artifact Chunk Saving**
- Tool: `saveArtifactChunks`
- Inputs: Session + artifact + gate metadata
- Expected: Redis stores chunked artifact, viewable via Redis CLI

#### 6. **Artifact Chunk Retrieval**
- Tool: `fetchArtifactChunk`
- Inputs: `session_id` + `chunk_id`
- Expected: Fetches Redis data for the correct chunk

#### 7. **Assemble Final Artifact**
- Toolchain: `assemble_artifact_chain`
- Inputs: Project profile + artifact metadata
- Expected: Merges formatted sections, stores to Drive, updates section text

---

### 🛠 Logging & Debug
- Validate Redis content via key: `artifact_chunks:{session_id}:{artifact_id}`
- Validate logs for toolchain inputs/outputs
- Check Drive for final artifact storage link

---

### 📥 Inputs Required
- Sample project text file (for upload)
- Project + session + artifact IDs
- Manually simulate Redis if chunking not triggered automatically

---

### 🧑‍💻 Instructions
- Run each test case locally using scripts or through `pytest`
- Capture stdout and logs for results
- Compare with `test_results_iteration_2.md` structure

---