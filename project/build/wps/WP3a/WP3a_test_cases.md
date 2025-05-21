# WP3a Test Cases – Planner + Memory Layer

## ✅ Test Goals
Ensure:
- Planner selects correct toolchain based on intent
- All tool runs are logged
- Session snapshots persist and reload correctly
- Replay mode works without triggering tools
- Trace YAML is accurate and complete

---

## 🧪 Test Case Matrix

### TC1: Run planner in live mode
- **Input**: Intent = `generate_section`, Inputs = `{section: outputs}`
- **Expected**:
  - Toolchain executed: `intent_classifier` → `schema_loader` → `section_writer`
  - Trace log created
  - JSONL log file updated
  - Session snapshot file created

### TC2: Run planner in replay mode
- **Input**: Mode = `replay`, same intent and inputs
- **Expected**:
  - Toolchain simulated using logs
  - No LLM/tools triggered
  - Outputs match previous live run

### TC3: Log structure test
- **Check**: PromptLog file contains valid entries (JSONL, keys match schema)

### TC4: Snapshot reload test
- **Check**: `load_latest_snapshot()` returns latest session state

### TC5: Trace YAML output test
- **Expected**: Planner returns reasoning trace with accurate tool steps

### TC6: Missing tool error
- **Input**: Intent with undefined toolchain
- **Expected**: Planner raises `ValueError`

### TC7: File path fallback
- **Test**: Output too large → logs written to file, DB stores path only (manually simulate)

---

## 🔁 Reusability
Tests can run as CLI, no UI dependency
- Example runner script to be added in WP3b

## 🔐 Notes
- Snapshot and log file location is hardcoded for now (adjust in prod)
- Future enhancement: Add checksums for trace validation