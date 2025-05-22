## WP12 Retrospective – Draft Generation Design Patch

### 🧠 What We Set Out to Do
Clarify where and how draft generation occurs in PolicyGPT, and define a design solution that supports:
- High-quality, evidence-based artifact drafting
- Seamless transition from structured user input to LLM-driven output
- Resilience to token and session limitations

### ✅ What Went Well
- Deep review of system files provided clear insights on planner-toolchain interactions
- Identified missing UX handshake step between user input and draft synthesis
- Mapped full data and memory flow from PromptLog to ArtifactSection
- Aligned LLM integration (`compose_and_cite`) with planner and user needs

### 🔍 Challenges
- Fragmentation between UI tools (WP16) and planner-triggered backend tools
- Need to balance dense generation with LLM token constraints
- Clarifying real-time user agency vs. automated flows

### 📈 Improvements
- Introduced confirmation prompt in GPT UI to smooth input-to-draft transition
- Defined chunking and memory-aware strategies to handle long documents
- Specified clear deliverables across tools, DB schema, YAMLs, and documentation

### 💡 Lessons Learned
- Even with agentic orchestration, human UX layers are critical to bridge gaps
- Every planner or LLM tool should explicitly log what memory and inputs it used
- Drive-based edit detection can simplify handoffs without breaking GPT context

### 📂 Outputs Committed
- `project/system_design/dense_artifact_generation.md`
- `project/build/wps/WP12/update_message.md`

### 📌 Next Suggestions
- Add flow diagram or sequence chart to visualize draft process
- Sync with WP16 to implement the GPT “Ready to Draft?” UI step
- Validate `compose_and_cite` tool coverage in test runs