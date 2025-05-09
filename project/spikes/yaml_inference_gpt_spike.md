## 🤖 Spike Report: YAML Inference in GPT – Concussion Recovery GPT App

---

### 🎯 Objective
Evaluate how a Custom GPT can best interact with structured medical YAML logic (e.g., `triage_map.yaml`, `stages.yaml`) to provide fluid, guided symptom triage and recovery advice. Compare using prompt-based context injection vs. tool-based access via FastAPI.

---

### 🔍 YAML Files in Scope
- **`triage_map.yaml`** – Triage question logic and follow-up conditions
- **`stages.yaml`** – Recovery stage logic with symptom + activity rules

---

### 🧪 Comparison: GPT Prompt Injection vs. Tool-Based Inference

#### 1. Prompt Injection
**Approach**: Embed the YAML logic inline as part of the GPT’s system prompt or context window.

| Pros                      | Cons                                     |
|---------------------------|------------------------------------------|
| Fast to prototype         | Maxes out token limits quickly            |
| Easier for user to edit   | No persistent memory of state            |
| Feels more fluid          | Harder to update logic centrally         |

#### 2. Tool-Based Inference
**Approach**: Use OpenAPI tools like `get_triage_question` and `get_stage_guidance` to access YAML logic stored server-side.

| Pros                                 | Cons                          |
|--------------------------------------|-------------------------------|
| Centralized logic, easier to maintain| Slightly more rigid UX       |
| Enables chaining and dynamic behavior| Requires tool call setup     |
| Supports multi-turn structured logic | Higher dev complexity initially |

---

### ✅ Recommendation: Tool-Based Access with Context Preload
- GPT should load structured logic (like triage flow or recovery stages) once per session via tools
- Tools like `get_triage_flow` and `get_stage_guidance` should:
  - Return the entire YAML logic graph or decision map
  - Let GPT interpret it conversationally to guide users
  - Enable structured triage without turn-by-turn rigidity
- GPT instructions should encourage **fluid Q&A** using the flow map, rather than re-calling tools after every reply
- GPT should access YAML logic using OpenAPI tools
- Tools like `get_triage_question` and `get_stage_guidance` should:
  - Load the YAML file in FastAPI backend
  - Parse logic and return relevant prompt content or decisions
  - Enable fluid GPT interaction while maintaining structure
- GPT instructions should encourage **follow-up Q&A** and **freeform phrasing**, not rigid slot-filling

---

### 🧰 Tools to Build

| Tool Name             | Purpose                                                |
|------------------------|---------------------------------------------------------|
| `get_triage_flow`     | Return full triage_map.yaml graph for inline reasoning |
| `get_stage_guidance`  | Return recovery advice from stage + data               |
| `assess_concussion`   | Consolidate triage inputs into summary                 |
| `get_triage_question` | Return next question based on history                  |

These tools can internally call YAML parsers and maintain session memory via `tracker_id`

---

### 🔍 Sample Use Case Flow (GPT + Tools)

1. **GPT** (calls `get_triage_flow`): Loads the full triage map logic at start of session
2. **User**: “My daughter got hit during soccer practice and has a headache.”
3. **GPT** (parses triage flow): “Was she dizzy or did she lose consciousness?”
4. **User**: “She was dizzy for a bit.”
5. **GPT** (evaluates symptom via flow + `flag_risk`): “This may be high risk. I recommend stopping play immediately.”
6. **GPT** (calls `create_tracker`): “Let’s start tracking recovery. What’s her age and sport?”

---

### 🧮 YAML Parsing Logic

The triage engine supports two modes:

#### 1. `get_triage_question` Mode (Step-by-step)
- GPT calls the tool after each user reply
- `triage_engine.py` determines the next node based on history
- Suited for controlled UX or linear flows

#### 2. `get_triage_flow` Mode (Context preload)
- GPT loads full triage_map.yaml at start
- `triage_engine.py` only parses and returns the structured flow graph
- GPT navigates it using natural reasoning

The stage engine remains consistent for both approaches:

#### `stage_engine.py`
- Loads `stages.yaml` defining recovery criteria for each stage
- Matches symptom and activity logs to current recovery stage
- Returns stage name, description, and next-step guidance

Both engines should include schema validation and support versioning for updates

---

### 🔗 Tool Chaining in GPT

Tool chaining refers to GPT calling one tool, interpreting its output, and using that result to trigger or guide the next tool call.

**Example Chain:**
1. `get_triage_flow` → loads full triage map
2. GPT asks follow-up questions based on parsed flow
3. Once symptoms are collected, GPT calls `flag_risk`
4. If risky, it can also call `create_tracker` or offer safety guidance

This chaining can be handled internally by the GPT logic, with minimal user intervention, and allows GPT to simulate an intelligent assistant navigating structured medical logic.

**Note:** GPT decides *when* to call each tool by:
- Interpreting tool descriptions in the OpenAPI schema (e.g. "Use this when symptoms are gathered")
- Following logic embedded in its custom GPT instructions (e.g. "Call `flag_risk` only after collecting all symptoms")

This gives GPT enough autonomy to orchestrate tools as needed, without requiring LangChain or an external router.

---

### 💬 Custom GPT Instructions
To make use of YAML inference tools effectively, the Custom GPT should be configured with these guidance principles:

- Load full triage or stage logic via tools at the start of the session (e.g., `get_triage_flow`)
- Use natural conversation to gather inputs (age, symptoms, sport) while consulting the flow map
- Only call downstream tools (e.g. `flag_risk`, `create_tracker`, `get_stage_guidance`) when confident based on collected responses
- Speak in empathetic, plain-language tones suitable for non-clinical users
- Clarify this is not a diagnosis, just structured guidance based on protocols

Custom instructions should also remind GPT to avoid excessive tool calls unless new information is available or the user's input requires structured escalation.

---

### 📌 Implementation Notes
- FastAPI will preload YAMLs in memory at startup
- YAML schemas should be versioned and validated
- GPT tool metadata will describe expected input/output (e.g. `question_context`, `tracker_id`, `symptoms[]`)

---

### ✅ Next Steps
- Define YAML parsing logic in `triage_engine.py` and `stage_engine.py`
- Build initial tool contracts in OpenAPI schema
- Update Custom GPT instructions to reflect conversational style with embedded tool chaining
- Simulate multi-turn chat to validate experience

---