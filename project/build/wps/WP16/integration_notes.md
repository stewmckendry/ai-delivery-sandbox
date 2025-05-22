# Integration Notes: Input UX + Memory Layer

## 🔗 Purpose
This doc summarizes how WP16 tools integrate with:
- PolicyGPT flows (guided prompts, data ingestion)
- The PromptLog + vector memory system
- Downstream tooling like `compose_and_cite`

---

## 🧰 Tool-to-System Integration

### inputPromptGenerator
- **Input**: `gate_id`, `artifact_id`, `section_id`
- **Output**: Structured user prompt block per gate reference
- **Uses**: `gate_reference_v2.yaml`
- **Integration**: Called by GPT to kick off structured data collection per section

### inputChecker
- **Input**: `gate_id`, `artifact_id`, `section_id`, `inputs`
- **Output**: Completeness status, missing intents
- **Uses**: `gate_reference_v2.yaml`, `prompt_schema.json`
- **Integration**: GPT can call it post-input to check if ready to draft

### loadCorpus
- **Input**: `file_contents`, `file_name`, `metadata`
- **Output**: Embeds content in vector DB
- **Integration**: Exposed to GPT for document ingestion workflows
- **Logged to**: PromptLog
- **Supports downstream**: Retrieval for `compose_and_cite`, `review_and_reflect`

### uploadTextInput / uploadFileInput / uploadLinkInput
- **Input**: Content + `metadata`
- **Output**: Logged input
- **Integration**: Memory and trace log
- **Supports**: Context and references for generation

---

## 🧠 Prompt Schema Alignment
- Core tools (inputPromptGenerator, inputChecker) use `prompt_schema.json`
- PromptLog records inputs with metadata to help align context
- Future tools (compose, planner) will read memory via metadata filters

---

## 🗃️ Trace + Memory Linkage
- All tools now log `gate`, `artifact`, `section`, `intent`, `session_id`, `user_id`
- PromptLog serves as the anchor for linking session data to draft generation
- Tools write structured traces for analysis and review

---

## Future Work
- Compose toolchain to use metadata + prompt schema to target memory slices
- Review UI to use prompt schema for user preview
- Consider vector DB migration from local to hosted (TBD)

---

Owner: WP16Pod