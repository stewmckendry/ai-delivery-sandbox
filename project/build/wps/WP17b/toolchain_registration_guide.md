# 🧰 Toolchain & Planner Guide (v2)

## 🧠 Overview
This guide explains how to define, register, and invoke toolchains using the `PlannerOrchestrator`. Toolchains are now implemented as separate classes for modularity and traceability.

---

## 🗂️ Toolchain Architecture
Each toolchain is a dedicated class (e.g., `GenerateSectionChain`) implementing a `.run(inputs)` method.

### Planner Routing
In `PlannerOrchestrator.run()`:
```python
if intent == "generate_section":
    return GenerateSectionChain().run(inputs)
```

---

## 🏗️ Create a New Toolchain

### 1. Create Toolchain Class
Put it in `app/engines/toolchains/your_chain.py`:
```python
class YourToolchain:
    def run(self, inputs):
        # Call tools in order, passing outputs as needed
        ...
```

### 2. Add to Planner
In `planner_orchestrator.py`, route the intent:
```python
if intent == "your_intent":
    return YourToolchain().run(inputs)
```

---

## 🧪 Tool Registration
Each tool in the chain must be:
- Implemented as a class with `run_tool()` and `validate()`
- Added to:
  - `project/reference/tool_catalog.yaml`
  - `project/reference/gpt_tools_manifest.json`

---

## 📘 Reference: WP17b Example
### Intent: `generate_section`
Class: `GenerateSectionChain`
Defined at: `app/engines/toolchains/generate_section_chain.py`
Steps:
1. `memory_retrieve`
2. `section_synthesizer`
3. `section_refiner`

Each tool receives structured inputs and passes results downstream.

---

## 🎯 Benefits
- 🔁 Modular toolchains with pre/post logic flexibility
- 🤖 Compatible with GPT calls
- 📜 Full execution trace included in results

Use this pattern for all Phase 2 toolchains.