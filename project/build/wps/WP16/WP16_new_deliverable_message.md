### 📬 New Deliverable for WP16: Draft Review UX Interface

**Deliverable:** `/ui/gpt_review_interface.md`

**What:**
Create a design spec and UX flow for a user-facing interface that:
- Summarizes the input context, project profile, and prior outputs
- Prompts the user to confirm readiness to begin LLM-powered draft generation

**Why:**
This component is part of the new drafting architecture defined in `dense_artifact_generation.md` (WP12). It ensures that users are informed and in control before the system invokes automated section generation.

**Who it Serves:**
- Users working through the custom GPT interface
- Downstream planner and toolchain layers that require user go-ahead before starting tool-based drafting

**Context & Reference:**
- See `dense_artifact_generation.md` for system design
- Coordinate with WP6 (logging draft confirmation), WP4 (draft generation tools)
- Ensure compatibility with existing UI and memory input structures

This item is now tracked in the `spillover_tracker.md`. It will be added to WP16’s official definition in the next revision.

Thank you! Let us know if you need further design guidance or coordination points.