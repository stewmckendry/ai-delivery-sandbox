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

### Batch 3: Journaling & Reflection + /save_reflection

**Scope:** Accept reflection input from GPT and save to Airtable + Notion

**Files:**
- `schemas/reflection.py`
- `routes/memory.py`
- `utils/memory_manager.py`
- `clients/airtable_client.py`
- `clients/notion_client.py`

**Spec Alignment:**
- Matches tech spec: Journaling / Reflection
- Implements memory interface in `memory_interface_design.md`

**Notes:**
- Pydantic model includes reflection length validator
- Clients are stubbed and tested with valid + invalid inputs
- Dual-write confirmed stub-safe for future API integration

---

### Batch 4: Summary View + /fetch_summary

**Scope:** Retrieve session reflections and provide a combined summary string

**Files:**
- `schemas/summary.py`
- `routes/memory.py`
- `utils/memory_manager.py`
- `clients/airtable_client.py`

**Spec Alignment:**
- Matches tech spec: Backend Memory (Optional)
- Aligns with GPT tool contract in `fastapi_and_gpt_scaffolds.md`

**Notes:**
- Combines all reflection texts into one output
- Handles empty session fallback
- Mocked Airtable read for now

---