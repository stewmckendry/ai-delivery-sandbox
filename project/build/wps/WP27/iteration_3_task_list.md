## ✅ WP27 – Iteration 3 Task List

### Phase 0: UX Implementation Scope (New)
1. **Implement summarization utility** to reduce long project inputs
2. **Create global_context toolchain** to run corpus + web + GoC alignment searches
3. **Refactor generate_section_chain** to:
   - Accept and use global_context
   - Fetch logged research instead of internal calls (no longer runs the tools)
4. **Validate section-by-section drafting mode** with end-to-end test

### Phase 1: Plan and De-risk
5. Define prompt contract for section generation [DONE]
6. Draft 2 dry run examples for 2 sections [DONE]
7. Draft feedback schema + simulate GPT checkpoint dialogs [✓ Iteration 4]

### Phase 2: Refactor for Global Context
8. Refactor generate_section_chain.py to remove direct calls to:
   - corpus search
   - web search
   - alignment search
   Instead, query memory for global_context results
9. Update section_synthesizer.py to accept:
   - prior_sections_summary
   - global_context
10. Patch prompt YAMLs for:
   - prior_sections_summary
   - global_context

### Phase 3: New Chain Logic
11. Create generate_artifact_chain.py:
   - Load section metadata
   - Query memory for global_context
   - Loop through each section
   - Compose and call generate_section_chain
   - Call assemble_artifact_chain

### Phase 4: Integration & Testing
12. Update test script for full artifact generation
13. Validate logs and prompt hydration across all tools
14. Manual test run + reasoning trace capture

### Phase 5: UX & GPT Flow
15. Insert GPT checkpoints between sections
16. Validate user feedback loop + flow UX
17. Optional: Add feedback logger to persist review state

### Phase 6: Polish + Debrief
18. Write iteration 3 test results + trace summary
19. Plan iteration 4 based on feedback + test results