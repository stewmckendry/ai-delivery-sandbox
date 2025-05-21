# Tool Registry System

This document explains the architecture and usage of the dynamic tool registry system implemented in WP3b for PolicyGPT.

---

## 🔧 Purpose
Enables standardized loading, invocation, and trace logging for all GPT-compatible tools and internal toolchain components.

---

## 🧩 Components

### 1. `tool_catalog.yaml`
- Central registry of tool metadata: tool ID, module path, class name
- Located at: `project/reference/tool_catalog.yaml`

### 2. `tool_registry.py`
- Dynamically loads tool classes from YAML
- Provides methods: `get_tool(tool_id)` and `list_tools()`
- Used by both CLI and API router

### 3. Tool Wrappers (`tool_wrappers/*.py`)
- Each defines a `Tool` class with a `.run_tool(input_dict)` method
- Optionally include CLI fallback for local testing

### 4. `api_router.py`
- Mounts `POST /tools/{tool_id}` endpoint
- Invokes tool via `ToolRegistry`
- Returns structured JSON output

---

## 📈 Usage Modes

### ✅ GPT Calls
- GPT can call tool by ID
- Response logged in YAML trace

### ✅ Internal Toolchains
- Other tools or chains can call `ToolRegistry().get_tool()` directly

---

## ⚙️ Extensibility
- Add entry in YAML → implement `Tool` class
- No API changes needed
- CLI, API, and toolchain ready by default

---

## 📌 Example

```yaml
# tool_catalog.yaml
translateDocument:
  module: app.tools.tool_wrappers.translateDocument
  class: Tool
```

```python
# tool_registry usage
registry = ToolRegistry()
tool = registry.get_tool("translateDocument")
result = tool.run_tool({"doc_id": "xyz", "target_lang": "fr"})
```

---

This modular setup accelerates new tool integration, standardizes I/O and supports fallback + trace at every stage.