### ✅ WP16 Patch Plan Update – Metadata Trace Logging to DB

#### 🧭 Context
Current trace logs are written to YAML files and referenced via `PromptLog.full_input_path`. These files contain rich info (input, output, metadata), but aren't usable in a cloud context or easily queryable.

#### ❗ Problem
Local trace files:
- Can't be queried via DB
- Aren’t portable or reliable in cloud
- Make filtering by metadata (e.g. `gate`, `artifact`) infeasible

#### 🎯 Solution
Augment the `PromptLog` schema to include a `metadata` JSON field and write trace metadata directly to the database.

---

### ✨ Patch Plan

**1. Design Doc**
- Define schema updates
- Specify how metadata should be written to `PromptLog`
- Formalize `metadata` block standard

**2. Update `structure_input`**
- Output metadata into a dict, not just YAML

**3. Update `log_tool_usage`**
- Accept and persist metadata as a new field in `PromptLog`

**4. Add new `metadata` column in PromptLog**
- `Column(JSON)`

**5. Update affected tools (uploadTextInput, etc.)**
- Collect metadata
- Pass to both trace file and DB

**6. Notify Lead Pod**
- File a CR explaining rationale, DB change, tool impacts

---

### 🧱 Impacts
- Adds new field to core DB model
- Requires cascade update across Pods
- Enables richer querying + cloud compatibility

---

### 📍 Next Steps
- [ ] Commit design doc
- [ ] Implement patch 1 tool at a time
- [ ] File CR to Lead Pod