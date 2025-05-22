## Design Patch: Human + Autopilot UX for Dense Artifact Drafting

### 📌 Objective

To define the integrated user experience and technical flow that supports both human-in-the-loop and autopilot generation of dense, evidence-based artifact sections for PolicyGPT. This design patch focuses on:
- Seamless user transition from input capture to draft review
- Planner-triggered drafting with OpenAI LLMs
- Chunked, memory-aware execution within token limits
- Full traceability and validation of generated content

---

### 🛠️ End-to-End Generation Process

#### 1. User Input (WP16 UI + WP9 Upload Tools)
- Users provide context via:
  - Structured prompts
  - Uploading files, links, or text
- Inputs are tagged by gate, artifact, section, and intent, and logged to `PromptLog`

#### 2. GPT UI Confirmation Step
- GPT summarizes user inputs
- Asks: "Ready to generate a first draft based on these inputs?"
- On confirmation, a Planner toolchain is triggered

#### 3. Planner Execution (WP3a)
- Loads:
  - `gate_reference.yaml`
  - `project_profile.yaml`
  - Tagged `PromptLog` entries
- Generates a plan saved to `planner_task_trace.yaml`

#### 4. Toolchain Execution: Drafting + Validation
- Executes steps like:
  - `searchKnowledgeBase`
  - `compose_and_cite` (LLM-powered)
  - `validateSection`
- Outputs written to:
  - `ArtifactSection` (draft)
  - `ReasoningTrace` (LLM steps)
  - `ValidationLog` (schema/logic check)

#### 5. Draft Review and Edit
- Draft shown in GPT UI with trace and feedback prompts
- User may:
  - Edit in GPT (revision triggers `revise_section`)
  - Edit in Drive (trigger revalidation)

#### 6. Finalization and Export
- On user sign-off or autopilot path:
  - Drafts committed to Drive
  - Version tracked in `DocumentVersionLog`
  - Diff, feedback, and approvals handled via Planner updates

---

### 🧠 Tools and Responsibilities

| Tool | Triggered By | Purpose |
|------|--------------|---------|
| `compose_and_cite` | Planner | Drafts section using OpenAI LLM + evidence |
| `searchKnowledgeBase` | Planner | Fetches internal/external support evidence |
| `validateSection` | Planner | Ensures required fields and logic pass |
| `revise_section` | GPT UI | Applies user feedback and revalidates |
| `get_token_usage` | Planner | Pre-check for token planning |

---

### 📃️ Data Sources and Memory Models

| Data Object | Format | Storage | Use in Generation |
|-------------|--------|---------|-------------------|
| `PromptLog` | SQL | DB | User inputs to section (structured metadata) |
| `ArtifactSection` | SQL | DB | Draft text content |
| `ReasoningTrace` | SQL/YAML | DB + local | Steps/tools GPT used |
| `ValidationLog` | YAML | local | Output of validation checks |
| `planner_task_trace.yaml` | YAML | local | Tool sequence for each section |
| `gate_reference.yaml` | YAML | local | Defines required fields |
| `project_profile.yaml` | YAML | local | Central context for drafting |

---

### 💡 User Experience Paths

#### Human-in-the-loop
- Input prompts → Confirm to draft → GPT presents draft
- User iterates in GPT or Drive
- GPT revalidates and logs reasoning

#### Autopilot
- User uploads all inputs and selects “Generate Full Artifact”
- Planner auto-runs each section
- GPT commits to Drive, logs full reasoning and validation
- User receives link + summary

---

### 📂 Drive Integration
- Each section is exported to Drive
- Version metadata and doc link saved in `DocumentVersionLog`
- Edits in Drive are detected and logged (webhooks or polling)
- GPT UI surfaces when edits are detected for validation

---

### 🔒 Technical Constraint Handling

#### Token Limits
- Section size scoped to 1,000–1,500 words
- Planner uses `get_token_usage` to check inputs
- If limit exceeded:
  - Inputs chunked
  - Drafts built in parts and stitched

#### Memory Constraints
- Full-document memory not loaded into GPT
- Instead, previous outputs summarized from:
  - `ReasoningTrace`
  - `ArtifactSection`
  - `DocumentDiff`

---

### ✅ Deliverables to Implement

| Path | Description |
|------|-------------|
| `/tools/compose_and_cite.py` | LLM drafting wrapper for planner use |
| `/tools/revise_section.py` | Feedback-based revision tool |
| `/tools/get_token_usage.py` | Pre-check for token planning |
| `/tools/validate_section.py` | Ensures schema, tone, required fields |
| `/ui/gpt_review_interface.md` | Summarize input + confirm draft interface |
| `/planner/templates/planner_task_trace.yaml` | Task orchestration schema |
| `/db/schemas/prompt_log.sql` | Input logs with gate/section metadata |
| `/db/schemas/artifact_section.sql` | Draft content storage |
| `/db/schemas/reasoning_trace.sql` | GPT chain-of-thought storage |
| `/db/schemas/document_version_log.sql` | Final doc commit logs |
| `/yaml/validation_log.yaml` | Section validator output YAML |
| `/yaml/project_profile.yaml` | Project inputs shared across sections |
| `/yaml/gate_reference.yaml` | Defines artifact structure |
| `/system/docs/dense_artifact_generation.md` | This design patch |

---

This patch defines a complete, scalable, and user-friendly model for generating complex, multi-section artifacts with GPT support — balancing user control with automated quality generation, while navigating technical constraints with memory-aware, chunked flows.