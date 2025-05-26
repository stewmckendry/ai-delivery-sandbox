## ✅ Test Plan: Generate Section Chain with Alignment and Corpus Tools

### 1. Objectives
- Validate correct end-to-end behavior of `generate_section_chain`
- Confirm integration and output of:
  - `queryPromptGenerator`
  - `queryCorpus`
  - `goc_alignment_search`
- Verify structured inputs passed to `section_synthesizer`

### 2. Setup Steps
- Ensure Railway remote Chroma is available and loaded
- Confirm OPENAI_API_KEY is valid
- Set environment variables as needed (`USE_REMOTE_CHROMA`, `CHROMA_HOST`)

### 3. Test Inputs
```json
{
  "artifact": "Digital Strategy",
  "section": "Open Government Policies",
  "project_profile": {
    "project_id": "P123",
    "title": "Open Government Data Initiative",
    "scope_summary": "Develop a federal policy to promote open data use",
    "strategic_alignment": "Supports Canada’s Digital Strategy and Data Governance",
    "key_stakeholders": "TBS, SSC, Statistics Canada",
    "project_type": "Policy"
  },
  "session_id": "test-session-001",
  "user_id": "dev-tester"
}
```

### 4. Test Steps
1. Call `generate_section_chain.run(inputs)`
2. Verify logs for each tool call (memory, search, query, corpus, alignment)
3. Inspect outputs:
   - `queryPromptGenerator`: returns 1-line query
   - `queryCorpus`: returns relevant corpus chunks
   - `goc_alignment_search`: returns GC.ca relevant citations
   - `section_synthesizer`: combines all into a prompt
   - `section_refiner`: refines draft
   - `save_artifact_and_trace`: persists to ReasoningTrace

### 5. Expected Results
- Outputs are returned and match format
- Draft is based on real evidence from embedded corpus + GoC alignment
- All entries appear in ReasoningTrace with relevant source logging