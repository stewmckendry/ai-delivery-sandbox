### WP27 – Toolchain Integration + GPT Wiring

**Objective:**
Wire existing toolchains and tool wrappers into the GPT interface to enable seamless interaction, exploratory testing, and agile enhancement cycles. Ensure end-to-end flows work from user prompt through document generation, incorporating validation, memory lookup, and section logic.

**Scope:**
- Integrate all toolchains (`assemble_artifact_chain`, `generate_section_chain`, `IngestInputChain`, `generate_full_artifact_chain`, `revise_section_chain`) into GPT interface
- Implement tool invocation via structured planner tasks
- Ensure rendering supports chunk-safe display, validation overlays, and user guidance
- Execute exploratory and E2E tests
- Capture enhancement ideas and implement high-value features
- Collaborate with WP24 and WP12 for context and architecture

**Deliverables:**
- GPT-invocable endpoints for each toolchain
- Full GPT-driven E2E tests across sample projects
- UX enhancements for validation and chunk display
- Documentation of toolchain-GPT mappings

**Dependencies:**
- Reference files: `gate_reference_v2.yaml`, tool wrappers, toolchains
- Design context from WP24, WP12

**Owner:** TBD
**Phase:** Phase 2