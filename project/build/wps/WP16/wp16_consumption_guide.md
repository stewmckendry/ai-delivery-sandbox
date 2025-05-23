## WP16 Tool Consumption Guide for Downstream Pods

This document summarizes how other work packages can use the tools and data outputs developed in WP16 to support downstream drafting, evidence retrieval, document generation, and feedback workflows.

---

### 🔧 WP16 Tools Overview
| Tool ID              | Purpose                                                                 |
|----------------------|-------------------------------------------------------------------------|
| `inputPromptGenerator` | Generates structured input prompts using gate_reference_v2.yaml          |
| `inputChecker`         | Validates completeness of section inputs based on intents                |
| `uploadTextInput`      | Accepts and logs freeform user inputs into PromptLog                     |
| `uploadFileInput`      | Extracts and logs contents from file inputs                              |
| `uploadLinkInput`      | Scrapes and logs content from provided URLs                              |
| `loadCorpus`           | Embeds and stores documents in the vector database                       |

---

### 🧠 How to Use These Tools

#### 1. Generating Draft Artifact Sections
- **Inputs Needed**: Section inputs logged via upload tools or `inputPromptGenerator`
- **How**: Query `PromptLog` using section metadata (gate, artifact, section)
- **Follow-up Tool**: `compose_and_cite` (planned) will use this data to create drafts

#### 2. Loading Foundational Reference Documents
- **Inputs Needed**: PDF/DOCX/etc. provided by user
- **How**: Use `loadCorpus` to embed documents
- **Follow-up Tool**: `queryCorpus` (future tool) for searching semantic matches from corpus

#### 3. Building Project Profile Section
- **Inputs Needed**: User responses and `project_profile_fields` in gate_reference
- **How**: Extract relevant fields from PromptLog
- **Follow-up**: Auto-fill profile section using `composeDraft`

#### 4. Review + Confirm Before Drafting
- **Inputs Needed**: All PromptLog entries for a session
- **How**: Use `createSessionSnapshot` to summarize inputs
- **Follow-up**: GPT shows summary + confirm-to-draft message using `inputChecker`

#### 5. Feedback and Iteration
- **Inputs Needed**: User responses to draft or reviews
- **How**: Tools will log feedback in PromptLog and use inputs for traceability
- **Follow-up**: `submitDocumentFeedback` and `logReasoningTrace`

---

### 📝 Developer Notes
- All tools output JSON-like manifests and log structured data to PromptLog
- Vector DB entries via `loadCorpus` store metadata for semantic linking
- All tools use consistent metadata block: gate_id, artifact_id, section_id, intent, etc.

---

### 📎 File References
- `project/reference/gate_reference_v2.yaml`
- `project/build/prompt_schema.json`
- `app/db/models/PromptLog.py`
- `app/tools/tool_wrappers/`
- `project/test/wps/WP16/WP16_test_plan.md`