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
- Updated to use GitHub raw URL fetch per deployment plan

---

### Batch 2: Career Card Generator + /get_yaml_segment

**Scope:** Fetch career segment YAMLs by category (e.g., STEM, Creative)

**Files:**
- `utils/yaml_loader.py`
- `routes/segments.py`

**Spec Alignment:**
- Matches tech spec section: Career Card Generator
- Follows architecture for RAG using GitHub-hosted YAML

**Notes:**
- Uses category slug to build raw URL
- Validated STEM file fetch via live GitHub read
- Supports GPT tool contract for segment loading

---