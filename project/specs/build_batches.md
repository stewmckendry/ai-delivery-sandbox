## 🔨 Build Batch Log: AI CareerCoach

---

### Batch 1: Prompt Loader + /load_prompt

**Scope:** Implements prompt loading for GPT using prompt ID

**Files:**
- `utils/prompt_loader.py`
- `routes/prompts.py`

**Spec Alignment:**
- Matches tech spec section: Prompt Selector UI
- Aligns with `fastapi_and_gpt_scaffolds.md`

**Notes:**
- Handles 404s and fetch errors with graceful GPT messages
- First tool endpoint for GPT contract

---