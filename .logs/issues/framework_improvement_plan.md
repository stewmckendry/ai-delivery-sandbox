### 🚧 Framework Improvement Plan – Delivery, Artifacts & Automation

---

## 🔧 1. Artifact Organization & Versioning

### Current State
- Artifacts like `data_flow_master.md` become duplicated (`v2`, `addendum`) to avoid overwriting.
- Scattered across `project/delivery` and feature folders.
- `memory.yaml` holds all metadata but not surfaced for humans.

### Proposed Change
- Use structured folders per major design domain:
  - `data_flow/`
  - `tool_catalog/`
  - `schema/`
  - `qa_and_test/`
  - `deployment/`
  - `feature_<name>/`
- Each folder contains:
  - `index.md` (auto-generated summary from memory)
  - `v1.md`, `v2.md`, `addendums/*.md`
  - `changelog.md` (rendered from `changelog.yaml`)

### Rationale
Minimizes clutter, improves traceability, and centralizes human/GPT lookup.

### Steps
1. Move existing artifacts into folders by topic.
2. Tag memory entries with `category`, `version_of`, etc.
3. Auto-generate `index.md` from memory.

---

## 🧠 2. Wire Logging Into Commits

### Current State
- Reasoning and chain-of-thought logs are optional.
- Logging requires extra manual steps after commit.

### Proposed Change
- Add `chain_of_thought` field to commit tool.
- If present, it logs to outputs/task folder + links to task.

### Rationale
Ensures decisions are captured with commits without additional burden.

### Steps
1. Extend `commitAndLogOutput` to accept reasoning fields.
2. Auto-write `chain_of_thought.yaml` under `project/outputs/<task>/`.

---

## ✅ 3. Simplify Task Lifecycle & Metadata

### Current State
- Tasks often not completed.
- Metadata lives in task.yaml but rarely surfaced.

### Proposed Change
- Reduce to two states: `open` and `done`.
- Auto-link commits to tasks via file path or explicit task_id.
- Auto-complete if a commit:
  - Is tagged with `#final` or
  - Includes phrase like "wraps task", "final update", or
  - Commits all paths listed in task.yaml `outputs`

### Rationale
Keeps flow light-touch but still structured.

### Steps
1. Add NLP rules + `#final` keyword to detect task closure.
2. On matching commit, mark task as `done`.
3. Render task status inline with `memory.yaml` for visibility.

---

## 🧪 4. Integrate QA + Deploy Early

### Current State
- QA and deploy are deferred or manual.
- Feature tasks rarely include these steps upfront.

### Proposed Change
- Add QA + deploy tasks to each feature.
- Use tools that:
  - Run tests with a one-line trigger
  - Deploy to staging and confirm via shared test route

#### One-line Test Trigger Example
```bash
pytest test/test_export_summary.py --disable-warnings --maxfail=1
```
- Commit hook runs this before merging any task tagged `#qa-required`.

#### Deploy with Staging Config Example
```python
# route: /test_feature?user_id=abc
# Tool spins up staging app using app/main.py and dummy data
response = requests.get("http://localhost:8000/test_feature?user_id=abc")
assert response.status_code == 200
assert "headache" in response.text
```

### Rationale
Makes QA frictionless and deployment testable before merge.

### Steps
1. Add deploy+test entries in each `task_list.md`.
2. Auto-inject `#qa-required` tag on final stage commits.
3. Create test stub files + config per feature.

---

## 📘 5. Surface `memory.yaml` + `changelog.yaml`

### Current State
- Updated on each commit, but not queried.

### Proposed Change
- Enable GPT queries to memory index.
- Render changelog by file or topic.

### Rationale
Improves visibility of structure + decision history.

### Steps
1. Enhance memory index with `feature`, `type`, `phase`.
2. Add `generate_index_from_memory()` utility.
3. Render domain changelogs from `changelog.yaml` per folder.

---

This plan addresses real-world friction in task usage, documentation sprawl, reasoning loss, and QA debt. Next step: apply this to active repo folders + tools.