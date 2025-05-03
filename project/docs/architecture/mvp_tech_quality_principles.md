## ✅ Tech Quality Principles for CareerCoach MVP

These are simple guidelines to keep the MVP reliable, observable, and evolvable.

---

### 1. ✅ Testing Strategy
- Use `pytest` for route and logic unit tests
- Use `httpx` for simulated API calls
- Run on GitHub Actions on PRs
- Focus on:
  - prompt loading
  - YAML parsing
  - memory writing/reading

---

### 2. ✅ Logging & Observability
- Use FastAPI logging + Railway console logs
- Log key events:
  - Tool call success/fail
  - YAML segment not found
  - Reflection save error
- No user data or text logged

---

### 3. ✅ Analytics (Anonymous)
- Optional: count sessions started using Redis or a flat file
- Log: `session_id`, timestamp, prompt_id (only)
- Display counts in CI or dashboard later

---

### 4. ✅ Rate Limiting
- No limits for MVP
- Monitor `/save_reflection` frequency in logs
- Add IP/session throttle if needed (via Starlette middleware)

---

### 5. ✅ Fallback/Error UX
- If tool call fails:
  - GPT returns: “Oops! I’m having trouble getting that info. Want to try a different path?”
  - Use `tool_call_fallback` responses in system prompt
- No empty GPT replies allowed

---

### 6. ✅ Schema Evolution
- YAML segments follow versioned folder (`v1/`, `v2/` if needed)
- Optional JSON Schema checker before load
- Validate fields: title, emoji, metaphor, traits, activities

---

These principles keep the system graceful under failure, easy to inspect, and ready to scale.