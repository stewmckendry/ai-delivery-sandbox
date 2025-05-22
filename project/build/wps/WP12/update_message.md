**Update – WP12 Design Patch Committed**

We've completed and committed the design patch: **Human + Autopilot UX for Dense Artifact Drafting**. This patch addresses:

- How input transitions to planner-triggered draft generation
- How OpenAI LLMs are orchestrated via the `compose_and_cite` tool
- Technical constraint handling for long, high-quality documents
- User flows for both interactive review/edit and autopilot
- Full data layer mapping: PromptLog, ArtifactSection, ReasoningTrace, YAML traces
- Integration with Drive and revalidation logic

The patch is available at:
`project/system_design/dense_artifact_generation.md`

This will guide both frontend and backend pod alignment and implementation.

Let us know if a diagram or end-to-end sequence chart would help next.