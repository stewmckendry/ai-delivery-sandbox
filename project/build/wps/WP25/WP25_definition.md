# WP25 Definition – GPT Tool Discoverability & Description

## 🧠 Summary
Enable GPT to better understand what tools are available, what they do, how to use them, and when to call them during document workflows.

## 🌟 Objective
Improve and operationalize GPT access to system tool documentation by:
- Expanding `gpt_tools_manifest.json` with schemas, I/O types, and call contexts
- Creating a browsable `tool_catalog.yaml` with GPT-readable summaries
- Developing a lightweight indexing tool (`tool_registry_builder`) to sync both sources

---

## 🧱 Deliverables
| File Path | Description |
|-----------|-------------|
| `project/reference/tool_catalog.yaml` | Rich tool descriptions for GPT lookup |
| `project/reference/gpt_tools_manifest.json` | Updated JSON manifest with enhanced fields |
| `app/tools/tool_utils/tool_registry_builder.py` | Builds and validates index from code + prompts |
| `project/build/wps/WP25/WP25_metadata_plan.md` | Field model and examples |
| `app/tools/tool_utils/fetchToolManifest.py` | GPT-callable tool to retrieve and embed manifest snapshot in session |
| `project/prompts/tool_discovery_scaffold.yaml` | GPT prompt examples for using tool list dynamically |

---

## 📐 Updated Tool Catalog Schema (YAML)

Each tool entry should include the following keys:

```yaml
tool_name:
  description: "What the tool does"
  module: "Python import path"
  class: "Python class name"
  usage: "When to use this tool"
  input_format: "YAML, JSON, text, etc."
  output_format: "Markdown, JSON, None, etc."
  dependencies: ["memory_retrieve", "externalWebSearch"]
  sample_call: |
    input:
      query: "Find risk strategies"
    expected_output: "Bullet summary of top docs"
  schema:
    type: object
    properties:
      query:
        type: string
    required:
      - query
```

Example:

```yaml
queryPromptGenerator:
  module: app.tools.tool_wrappers.query_prompt_generator
  class: Tool
  description: Generates a semantically rich natural language query from project profile and memory
  usage: Used to synthesize queries for searching external or internal corpora
  input_format: object
  output_format: string
  dependencies: []
  sample_call: |
    input:
      project_profile:
        goal: "Reduce emissions"
      memory:
        - input_summary: "Uploaded climate plan"
    expected_output: "What strategies has the city proposed to reduce emissions?"
  schema:
    type: object
    properties:
      project_profile:
        type: object
      memory:
        type: array
    required:
      - project_profile
      - memory
```

**Additions Needed:**
- Add usage, input_format, output_format, dependencies, and sample_call fields to each tool in tool_catalog.yaml.

## 🧾 Updated Manifest Schema (JSON)

Each tool should include:

```yaml
{
  "tool_id": "tool_name",
  "description": "What the tool does",
  "usage": "When to use this tool",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" }
    },
    "required": ["query"]
  },
  "output_type": "markdown",
  "dependencies": ["memory_retrieve", "externalWebSearch"],
  "example_call": {
    "query": "Find risk strategies"
  }
}
```

Example:

```json
{
  "tool_id": "compose_and_cite",
  "description": "Orchestrates evidence search, synthesis, and drafting of artifact sections.",
  "usage": "Used during artifact drafting to generate a section based on uploaded inputs, corpus, and web knowledge.",
  "input_schema": {
    "type": "object",
    "properties": {
      "section_type": { "type": "string" },
      "project_id": { "type": "string" },
      "gate_stage": { "type": "string" },
      "manual_inputs": { "type": "string" }
    },
    "required": ["section_type", "project_id", "gate_stage"]
  },
  "output_type": "markdown",
  "dependencies": ["memory_retrieve", "web_search", "validate_section"],
  "example_call": {
    "section_type": "risk_analysis",
    "project_id": "project-xyz",
    "gate_stage": "gate_3",
    "manual_inputs": "Review stakeholder interview from May 4th"
  }
}
```

**Additions Needed:**
- Add usage, dependencies, output_type, and example_call fields to each entry in gpt_tools_manifest.json.

---

## 🧭 GPT Bootstrapping + Catalog Retrieval

### Design Assumptions

- GPT loads tool context at start of session and when rehydrating from a memory snapshot
- Context is provided through a system prompt scaffold (e.g., “You have access to X tools described in...”)
- Optionally GPT calls a tool to fetch and cache manifest if not loaded or if tools change mid-session

### 🔧 GPT Tool Context: How It Gets Implemented


1. System Prompt Scaffold

**What:**  
A pre-set instruction loaded at session start to orient GPT about available tools.

**Example:**
System Prompt:
You are a policy co-pilot with access to a suite of tools. These tools include:
- compose_and_cite: for drafting content from inputs
- validate_section: for checking structure and tone
- uploadTextInput: for ingesting raw notes
Use the manifest described at tool_catalog.yaml or call fetchToolManifest to learn more.

**Location:**  
- Embedded in GPT system prompt config
- Or injected via `planner_prompts.yaml` at task setup

---

2. Start-of-Session Manifest Fetch

**Mechanism:**
- GPT either:
  - Loads a pre-injected summary of `gpt_tools_manifest.json`, or
  - Calls `fetchToolManifest` to retrieve a filtered live version

**Tool Required:**
- `fetchToolManifest.py`  
  Returns active tools filtered by context (project, gate, etc.)

**Optimization:**
- Pre-trim manifest to ~500–1000 tokens
- Group by use case: “artifact generation”, “feedback revision”, etc.

---

3. Rehydration from Snapshot

**Scenario:**  
Session crash, long pause, or token limit breach requires tool re-brief.

**Behavior:**  
- GPT receives rehydration prompt:
You’ve been rehydrated. Re-fetch the current manifest and resume planning from last trace step.
- Calls `fetchToolManifest` again
- Rebuilds planner state using `ReasoningTrace`, `PromptLog`

**Tracking:**  
- Store `last_manifest_version` in session memory
- Detect changes to re-trigger load

---

## ⚙️ Technical Design Notes

- Manifest is built at deploy time or on-demand using `tool_registry_builder`
- GPT receives simplified summaries (~2-3 lines/tool) with:
  - Tool name
  - Function
  - Required inputs + expected outputs
  - When to use / limitations
- Manifests and catalogs are versioned to reduce session bloat

---

## 🧠 Caching + Token Control Guidance

- GPT should **not fetch full manifest on every call**:
  - Only at session start or context reset
  - Use cached summary in session memory or tool.json file
- If tools are updated mid-session:
  - Use `fetchToolManifest` and `tool_diff_summary` to re-brief GPT on changes
- Embed only **active tools** for current project/gate using `projectProfile` filter

---

## ✅ Task Breakdown

| Task | Owner | File(s) |
|------|-------|---------|
| Build `fetchToolManifest` | WP25 | `tool_utils/fetchToolManifest.py` |
| Extend manifest builder | WP25 | `tool_registry_builder.py` |
| Write system prompt scaffold | WP25 | `tool_discovery_scaffold.yaml` |
| Test manifest parsing in GPT | WP25 | `test_tool_registry_builder.py` |
| Optional endpoint | WP25 | `/tools/query_available_tools` (if dynamic fetch enabled) |
| Introduce tools + manifest to GPT in system instructions | System prompt scaffold |
| Avoid token bloat | Use filtered manifest scoped to current gate/project |
| Track changes | Use manifest version tags |

---

## 🔁 Integration
- Referenced by GPT in tool planning, search, and selection flows
- Used in bootstrapping new GPT pods and for reindexing tools

---

## 🧪 Testing
| File Path | Description |
|-----------|-------------|
| `project/test/wps/WP25/test_tool_registry_builder.py` | Validates JSON+YAML integrity and link resolution |

---

## 🔮 Future Extensions
- GPT agent memory to cache and suggest commonly used tools
- Endpoint for querying tool metadata at runtime: `/tools/query_available_tools`
- Support for tagging tools with SDLC phase, persona, input style, and PoD ownership