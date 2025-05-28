## ✅ WP27 – Iteration 3 Task List

### Phase 1: Plan and De-risk
1. **Define prompt contract** for section generation
2. **Draft 2 dry run examples** using real inputs for 2 sections
3. **Build summarization utility** to truncate prior section content
4. **Draft feedback schema + simulate GPT checkpoint** dialogs

### Phase 2: Refactor for Global Context
5. **Refactor `generate_section_chain.py`** to isolate:
   - corpus search
   - web search
   - alignment search
   - outputs as `global_context`
6. **Update `section_synthesizer.py`** to accept:
   - `prior_sections_summary`
   - `global_context`
7. **Patch prompt YAMLs** for:
   - `prior_sections_summary`
   - `global_context`

### Phase 3: New Chain Logic
8. **Create `generate_artifact_chain.py`** to:
   - Load section metadata from `gate_reference`
   - Run global research
   - Loop through each section
   - Compose and call `generate_section_chain`
   - Accumulate results
   - Call `assemble_artifact_chain`

### Phase 4: Integration & Testing
9. **Update test script** for full artifact generation test
10. **Validate logs and prompt hydration across all tools**
11. **Manual test run + reasoning trace capture**

### Phase 5: UX & GPT Flow
12. **Insert GPT checkpoints** between sections
13. **Validate user feedback loop + flow UX**
14. **Optional: Add feedback logger to persist review state**

### Phase 6: Polish + Debrief
15. **Write iteration 3 test results + trace summary**
16. **Plan iteration 4 based on feedback + test results**