## Iteration 5 — Pre-Research Questions and Answers

### Question 1: Are there any specific files or submodules within the ai-delivery-sandbox repo that should be prioritized beyond what you've already listed (e.g., planner_orchestrator.py, tool_registry.py, app/prompts/)?

**Answer:** Yes, please also prioritize:
- `app/engines/toolchains/` (toolchain implementations)
- `app/tools/tool_wrappers/` (tool implementations)
- `main.py`, `api_router.py` (API routing and entrypoints)
- `openapi.json` (exposed API schema)
- `app/models/` (data models, if referenced)

These are critical to understanding execution paths and integration surfaces.

### Question 2: Would you like this report to include diagrams (e.g., architecture flowcharts or data flow diagrams), and if so, do you have a preferred format?

**Answer:** Yes, please include the following diagrams:
- System Architecture Overview
- Toolchain Execution Flow
- Data Flow for Memory and Embeddings

Format: Embedded within Markdown if possible. Optionally include as downloadable SVG/PNG if your tools support that.

### Question 3: Should the output be structured as a downloadable technical blueprint (e.g., Markdown or PDF), or are you looking for a plaintext answer directly in this chat?

**Answer:** Markdown format is preferred. A downloadable `.md` or `.pdf` file is ideal for repo integration. Plaintext is acceptable if easier to produce inline.

### Update: Latest User Flow Reference
The current user flow reference is now stored at:
`project/build/wps/WP27b/policygpt_custom_gpt_guide.md`
This supersedes the older `policygpt_user_flow.md` and should be treated as the primary source of flow context.