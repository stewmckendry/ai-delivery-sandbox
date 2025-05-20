## WP ID: WP16
## WP Name: Input Prompt UX Layer

### 🌟 Outcome  
By the end of this WP, as a **policy drafter**, I will receive guided prompts that ensure I provide relevant and complete inputs for drafting gate documents. This increases clarity, reduces back-and-forth, and accelerates document creation.

### 🧽 Scope  
**In Scope:**
- Generate dynamic prompts for users based on artifact and gate requirements
- Validate inputs and prompt users to fill gaps or clarify ambiguous submissions
- Use metadata from `gate_reference.yaml` to tailor prompts per artifact section
- Support both structured (guided prompt) and unstructured (data dump) input modes
- UX interface is the custom GPT chat experience

**Out of Scope:**
- Final document generation (WP1a)
- Evidence lookup or citation insertion (WP8)
- Manual UI frontend (future UI WP)

### 📦 Deliverables  
| File Path | Description |
|-----------|-------------|
| `app/tools/input_prompt_generator.py` | Creates context-aware prompts for input collection, driven by artifact and gate metadata |
| `app/tools/input_checker.py` | Scans provided inputs to flag missing fields or unclear content |
| `config/prompt_templates.yaml` | Stores reusable prompt templates with variables tied to `gate_reference.yaml` |

### 📄 Supporting Documentation (to generate)  
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP16/WP16_prompt_flows.md` | Example flows of prompt generation and user interaction |
| `project/build/wps/WP16/WP16_prompt_templates_spec.md` | Template syntax and gate-based customization logic |

### ✅ Acceptance Criteria  
- [ ] User is prompted with relevant questions based on selected gate and artifact
- [ ] Inputs are checked for completeness and clarity before draft starts
- [ ] System supports both structured and freeform input flows
- [ ] Prompt templates are reusable and customizable via config

### 🛠 Tasks  
| Task ID | Description |
|---------|-------------|
| T1 | Design prompt format and metadata variables |
| T2 | Build generator that reads from gate metadata and assembles questions |
| T3 | Implement input checker for completeness and ambiguity |
| T4 | Write prompt templates and store in YAML |
| T5 | Write sample test flows for input capture |

### 📚 Reference Documentation  
| File Path | Usage |
|-----------|--------|
| `gate_reference.yaml` | Defines expected inputs per gate and artifact |
| `tool_catalog_v2.md` | Describes prompt generator toolchain |
| `session_memory_model_v2.md` | Reference on how inputs feed into planner and memory trace |

### 📝 Notes to Development Team  
- Prompts should adapt dynamically to input type (e.g., file, free text)
- Should support "prompt again" behavior if content is missing
- Coordinate closely with WP1a for handoff of parsed inputs
- Toggle support for **guided prompt mode** vs. **data dump mode** should be built-in

### 🧠 Clarifications  
- 💡 This UX layer is logic-only; no UI is implemented here (future UI WP)
- 📥 Inputs can be parsed from chat history, uploaded files, or explicit form fields
- ♻️ Connects tightly with planner initiation and section drafting kickoff