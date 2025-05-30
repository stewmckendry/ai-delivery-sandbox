**When to Use section_review_feedback vs revise_section_chain**

### Overview

| Scenario | Use This Chain | Description |
|---------|----------------|-------------|
| Initial draft feedback | `section_review_feedback` | Collects user feedback after initial draft generation, structures feedback, maps to sections, and rewrites with revision trace. |
| Targeted revision to one or more sections | `revise_section_chain` | Directly revises sections based on feedback already mapped to section(s). Used when revision scope is known. |

### Guidance for GPT Custom Chat UI

**Use `generate_section_chain` first** to create initial sections.

Then:
- Prompt user for feedback across any or all sections.
- Call `section_review_feedback` to:
  1. Normalize and split feedback
  2. Map to affected sections
  3. Revise sections using `revise_section_chain`
  4. Store revised drafts + diff summaries in Redis
  5. Iterate review one section at a time in chat

After all feedback is reviewed, call `assemble_artifact_chain` to finalize and push to Drive.

### Visual Flow
```
User feedback (structured/unstructured)
        |
        v
section_review_feedback
        |
        +-- feedback_structurer: normalize + assign
        +-- revise_section_chain per section
               |
               +-- memory + feedback context
               +-- generate revision
               +-- diff_summarizer
               +-- Redis staging
        |
        v
GPT iterates: show user changes per section
        |
        v
User confirms all
        |
        v
assemble_artifact_chain
```

### Notes
- GPT is responsible for feedback collection and iterative interaction.
- Toolchains handle structured processing, revisions, and state management.
- Redis keying pattern ensures artifact + session-scoped review.