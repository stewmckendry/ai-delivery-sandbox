# WP26 Definition – Composable Planner: User-Configurable Chain Builder

## 🧠 Summary
Design a flexible, UI-integrated planner that enables users (or GPT) to configure which tools and steps to include in a document generation workflow.

## 🎯 Objective
Build a "composable" planner framework that:
- Allows chain-of-tools selection based on project profile, artifact type, and user preference
- Offers GPT-readable YAML scaffolds for flow definition
- Enables UI prompts to gather config and apply defaults

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/planner/composable_planner.py` | Core planner class with template loading, validation, execution hooks |
| `project/reference/planner_templates/*.yaml` | YAML templates for Risk Plan, Gate Brief, etc. |
| `project/prompts/planner_prompts.yaml` | GPT bootstraps for plan configuration dialogue |
| `project/build/wps/WP26/WP26_planner_architecture.md` | Internal system design for plan execution control |

---

## 🔁 Integration
- Used by GPT to populate and run toolchain flows
- Can replace hardcoded `generate_full_artifact_chain`

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `test_composable_planner.py` | Tests: config parse, defaulting, error handling |

---

## 🔮 Future Extensions
- GUI visual chain builder
- Planner preview and dry-run mode
- Embedding plan metadata in ReasoningTrace

---

## 🧭 Example User Flow

### Step-by-Step
| Step | Actor | Action | Input | Output |
|------|-------|--------|-------|--------|
| 1 | GPT | Prompts: “Which steps do you want in your workflow?” | Chat | Plan config scaffold |
| 2 | User | Replies: “Retrieve memory, then generate, refine, validate, commit” | List of steps | Plan YAML |
| 3 | GPT | Generates YAML plan using defaults | Tool list | `planner_templates/<artifact>.yaml` |
| 4 | Planner | Loads YAML and validates | Template | Executable plan |
| 5 | GPT | Narrates each step as it runs | Plan YAML | Real-time status in chat |
| 6 | Planner | Executes chain and logs trace | Inputs | Trace, outputs, Drive file |