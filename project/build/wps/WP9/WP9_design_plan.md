

---

### 📦 Input Storage Coverage — Current vs. Planned

#### ✅ Done:
- YAML trace logs (`logs/ingest_traces/*.yaml`) created for each input
- Tools output replayable metadata-rich input summaries
- CLI-compatible and schema-aligned ingestion

#### 🔜 Not Yet Implemented:
- `PromptLog` DB writes via `memory_sync.py`
- `SessionSnapshot` population for aggregate memory
- Retry handler (`retry_ingestion.py`) stubbed but not wired

---

### 📋 Updated Remaining Tasks:
1. **DB Writes**: Integrate `memory_sync.py` to log each input into `PromptLog`
2. **Session Snapshot**: Capture a session-level snapshot after batch ingestion
3. **Test Harness**: Validate both logs and DB records
4. **Retry Path**: Wire in retry logging for failed or malformed inputs
5. **Deploy Hooks**: If DB or memory setup needs init in Railway
6. **Completion Note**: Include DB + trace coverage summary