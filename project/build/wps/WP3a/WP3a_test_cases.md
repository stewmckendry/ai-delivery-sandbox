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
```bash
python -c "from app.engines.planner_orchestrator import PlannerOrchestrator; \
  print(PlannerOrchestrator(mode='live').run('generate_section', {'section': 'outputs'}))"
```
- **Expected**:
  - Toolchain executed: `intent_classifier` → `schema_loader` → `section_writer`
  - Trace log created
  - JSONL log file updated
  - Session snapshot file created

### TC2: Run planner in replay mode
```bash
python -c "from app.engines.planner_orchestrator import PlannerOrchestrator; \
  print(PlannerOrchestrator(mode='replay').run('generate_section', {'section': 'outputs'}))"
```
- **Expected**:
  - Toolchain simulated using logs
  - No LLM/tools triggered
  - Outputs match previous live run

### TC3: Log structure test
- **Check**: Open `logs/prompt_logs.jsonl`
- **Expected**: Each line is valid JSON with keys: `timestamp`, `tool`, `input`, `output`

### TC4: Snapshot reload test
```bash
python -c "from app.engines.memory_sync import load_latest_snapshot; \
  print(load_latest_snapshot())"
```
- **Expected**: Dictionary of most recent session state

### TC5: Trace YAML output test
- **Check**: Output of TC1 or TC2 includes full reasoning trace list

### TC6: Missing tool error
```bash
python -c "from app.engines.planner_orchestrator import PlannerOrchestrator; \
  PlannerOrchestrator().run('unknown_intent', {})"
```
- **Expected**: Raises `ValueError: No toolchain defined for intent: unknown_intent`

### TC7: File path fallback
- **Test**: Manually simulate large output in tool run and ensure logs write reference to file instead of inline text (future extension)

---

## 🔁 Reusability
- CLI-based testing ensures minimal dependencies
- Future: convert to unit tests or CLI script wrapper

## 🔐 Notes
- Adjust paths if running from non-root directory
- Log files are stored in `logs/` by default