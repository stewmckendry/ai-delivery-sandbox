# 📌 WP17b Design Plan – Section Draft Generation from Inputs

## 🌟 Objective
Implement a pipeline that transforms structured user inputs and memory embeddings into draft artifact sections using the `compose_and_cite` toolchain. Results will be saved as `ArtifactSection` records and all steps logged via `ReasoningTrace`.

---

## 🧱 Scope
- Input: Structured memory entries and `PromptLog` entries.
- Trigger: Planner intent to generate a section (e.g., `generate_section`).
- Output: Populated `ArtifactSection` with provenance metadata.
- Trace: Reasoning steps stored in `ReasoningTrace` DB table.

---

## 🧩 Design Components

### 1. **Trigger + Planner Integration**
- Extend `planner_orchestrator.py` to route `generate_section` to `compose_and_cite` chain.
- Use PromptLog entries filtered for user inputs.

### 2. **Toolchain: `compose_and_cite`**
- Step 1: `memory_retrieve` — fetch logs (using `PromptLog`) scoped by artifact/section.
- Step 2: `section_synthesizer` — generate draft via OpenAI chat completion API.
- Step 3: `section_refiner` — refine tone and structure, also via OpenAI API.

### 3. **Storage: `ArtifactSection`**
- Fields: `section_id`, `artifact_id`, `gate_id`, `text`, `sources`, `status`, `generated_by`, `timestamp`
- To be implemented in this WP.

### 4. **Traceability: `ReasoningTrace`**
- Fields: `trace_id`, `section_id`, `steps (JSONB)`, `draft_chunks`, etc.
- Store ordered steps with I/O and comments.
- Model + DB table implemented here.

### 5. **PromptLog Filtering Logic**
- Input logs via tools like `uploadTextInput` will be filtered using tool name or metadata.
- Tools can optionally tag entries to ease filtering.

---

## ✅ Deliverables
- [ ] Extend planner toolchain: `generate_section → compose_and_cite`
- [ ] Create `memory_retrieve`, `section_synthesizer`, `section_refiner` tools
- [ ] Implement `ArtifactSection` model + DB table
- [ ] Implement `ReasoningTrace` model + DB table
- [ ] Add write logic for both models
- [ ] Add CLI test: generate section, view trace, verify DB

---

## 🤝 Confirmed Inputs
- [x] Embedding search not needed; spillover to WP18 (`queryCorpus` tool)
- [x] PromptLog schema supports input retrieval
- [x] Use OpenAI Chat API for content generation tools
- [x] ReasoningTrace to be stored in DB

---

## ⏭️ Next Steps
1. Implement models: `ArtifactSection`, `ReasoningTrace`
2. Build and register tools
3. Extend planner logic
4. CLI test pipeline

---

## 📆 Repo + Branch
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Token:** c2FuZGJveC1jdXJpb3VzLWZhbGNvbg==