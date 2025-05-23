# 📌 WP17b Design Plan – Section Draft Generation from Inputs

## 🎯 Objective
Implement a pipeline that transforms structured user inputs and memory embeddings into draft artifact sections using the `compose_and_cite` toolchain. Results will be saved as `ArtifactSection` records and all steps logged via `ReasoningTrace`.

---

## 🧱 Scope
- Input: Structured memory entries and `PromptLog` entries.
- Trigger: Planner intent to generate a section (e.g., `generate_section`).
- Output: Populated `ArtifactSection` with provenance metadata.
- Trace: Chain-of-thought logging in `ReasoningTrace`.

---

## 🧩 Design Components

### 1. **Trigger + Planner Integration**
- Extend `planner_orchestrator.py` to route `generate_section` to `compose_and_cite` chain.
- Use `PromptLog` entries and memory embeddings as initial context.

### 2. **Toolchain**: `compose_and_cite`
- Step 1: `memory_retrieve` – fetch relevant logs and snapshots.
- Step 2: `section_synthesizer` – draft content with citations.
- Step 3: `section_refiner` – post-process output for tone, format, and completeness.

### 3. **Storage**
- Map outputs to `ArtifactSection` schema.
- Include fields: `section_id`, `artifact_id`, `gate_id`, `text`, `sources`, `status`, `generated_by`, `timestamp`

### 4. **Traceability**
- Each tool logs via `log_tool_usage`.
- Final trace and output stored in `ReasoningTrace` YAML.

---

## ✅ Deliverables
- [ ] Extend planner toolchain: `generate_section → compose_and_cite`
- [ ] Implement `memory_retrieve` wrapper tool
- [ ] Implement `section_synthesizer` tool
- [ ] Implement `section_refiner` tool
- [ ] Add `ArtifactSection` write logic
- [ ] Ensure logs in `PromptLog`, snapshots, and ReasoningTrace
- [ ] Add CLI test script to trigger section generation

---

## 🤝 Assumptions for Review
- `ArtifactSection` model is implemented or will be included in this WP.
- Toolchain steps can assume access to embeddings or will mock for initial phase.
- ReasoningTrace format is YAML + summary string (can evolve).

---

## ⏭️ Next Steps
1. Get Human Lead approval.
2. Build each component (toolchain, tools, logger, DB write).
3. Commit and test end-to-end flow using CLI.
4. Share test results and request deployment.

---

## 🔖 Repo + Branch
- **Repo:** `ai-delivery-sandbox`
- **Branch:** `sandbox-curious-falcon`
- **Token:** c2FuZGJveC1jdXJpb3VzLWZhbGNvbg==