# 🤖 ChatGPT Pre-Research Q&A – Iteration 2

## GPT Questions
1. Are there any specific folders or modules you want prioritized (e.g., api, tools, chains, etc.)?
2. Should I assume that all active features of GovDoc Copilot are hosted in this repo, or do they depend on external services/codebases as well?
3. Should the outputs include proposed implementation strategies (e.g., for reimplementation in another framework/language), or just diagnostics and artifact extraction?

## Response
1. Please prioritize the following key folders: `toolchains`, `tool_wrappers`, `prompts`, `db`, and `redis`. Key top-level files to start from or reference include: `openapi.json`, `main.py`, `api_router.py`, `tool_registry.py`, `planner_orchestrator.py`, `memory_sync.py`, `tool_catalog.yaml`, and `gate_reference_v2.yaml`.

2. Assume all active functionality for GovDoc Copilot is hosted in this repo. If you detect stubs or placeholders for external services, note them, but don’t explore beyond this codebase.

3. Focus on diagnostics and artifact extraction (user stories, design decomposition, test outline, modernization). Implementation strategies are not required in this iteration.