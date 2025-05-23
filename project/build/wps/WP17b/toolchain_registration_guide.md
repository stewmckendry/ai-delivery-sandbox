# 🧰 Toolchain & Planner Guide

## 🧠 Overview
This guide documents how to define, register, and invoke toolchains using the `PlannerOrchestrator` framework. It also covers registration of individual tools to ensure they can be used standalone (e.g., by GPT or CLI).

---

## 🗂️ Toolchain Architecture
Toolchains are sequences of tools triggered by planner "intents". For example:

```python
def select_tool_chain(self, intent: str):
    if intent == "generate_section":
        return ["memory_retrieve", "section_synthesizer", "section_refiner"]
```

### Components
- **PlannerOrchestrator** (`app/engines/planner_orchestrator.py`) handles toolchain execution and logging.
- **Tool Catalog** (`project/reference/tool_catalog.yaml`) maps tool_id to Python module and schema.
- **Tool Manifest** (`project/reference/gpt_tools_manifest.json`) exposes tool metadata to GPT.

---

## 🛠️ Registering a Toolchain

### Step 1: Define Tool Logic
Create your tools under `app/tools/tool_wrappers/`. Each should follow this pattern:

```python
class Tool:
    def validate(self, input_dict):
        pass
    def run_tool(self, input_dict):
        return {...}
```

### Step 2: Register Tools
Add tool metadata to:
- `project/reference/tool_catalog.yaml`
- `project/reference/gpt_tools_manifest.json`

Example:
```yaml
tools:
  section_synthesizer:
    module: app.tools.tool_wrappers.section_synthesizer
    class: Tool
    description: Generates draft section text
    schema:
      artifact: {type: string}
      section: {type: string}
```

### Step 3: Define Toolchain in Planner
Open `planner_orchestrator.py` and modify `select_tool_chain`:
```python
def select_tool_chain(self, intent: str):
    if intent == "generate_section":
        return ["memory_retrieve", "section_synthesizer", "section_refiner"]
```

### Step 4: Run via Planner
Call planner in code or CLI:
```python
from app.engines.planner_orchestrator import PlannerOrchestrator
planner = PlannerOrchestrator()
planner.run("generate_section", {"artifact": "...", "section": "..."})
```

---

## 🔄 Design Philosophy
- Toolchains should be modular — each step is a standalone tool.
- Tools should be callable by humans (via CLI) and by GPT (via manifest).
- Planner should orchestrate without needing internal knowledge of tool logic.

---

## ✅ Reference: WP17b
Toolchain: `generate_section`
Steps:
- `memory_retrieve` — gathers relevant inputs
- `section_synthesizer` — drafts raw section
- `section_refiner` — polishes tone/structure

Implemented under:
- `app/tools/tool_wrappers/`
- `app/engines/planner_orchestrator.py`
- `project/reference/tool_catalog.yaml`
- `project/reference/gpt_tools_manifest.json`

---

Use this pattern to add new toolchains across WPs in Phase 2.