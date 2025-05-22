## WP17 – Prompt Patterns and Templates

### 🎯 Objective
Design and manage the prompt templates, slotting logic, and reusable examples that guide GPT-driven drafting across PolicyGPT's tools and user flows.

### 📦 Scope of Work
- Design and catalog reusable prompt patterns used in:
  - compose_and_cite
  - compose_with_guidance
  - policy_to_artifact_chain
  - summarizeMemoryChunk
- Establish slotting logic for inserting memory facts, document context, and prior examples
- Create YAML format for defining prompt templates
- Design evaluation hooks to test prompt performance (clarity, completeness)
- Coordinate with WP4 and WP2 for tool integration

### 🔗 Dependencies
- Input from WP4 on synthesis tools
- Input from WP2 on memory chunk structure
- Input from WP9 on session memory format

### 📥 Inputs
- Memory chunks from WP2 and WP9
- Tool invocation context (gate, artifact, section)

### 📤 Outputs
- Library of prompt templates in YAML format
- Utility functions to resolve and slot prompt values
- Documentation and guidance for downstream Pods

### 🧠 Notes
- This WP does not call the GPT API directly, but enables other tools to do so in a controlled, consistent manner.
- This improves reuse, clarity, and traceability across smart drafting tasks.