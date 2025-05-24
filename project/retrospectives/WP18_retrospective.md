## WP18 Retrospective – Artifact Assembly and Routing

### ✅ What Went Well
- Strong modular architecture using toolchains and registries.
- Effective schema validation and logging throughout.
- Collaboration was smooth; feedback loop quickly applied to resolve issues.
- Test coverage was practical and caught meaningful edge cases.
- Final output quality is production-ready (clean format, ToC, markdown).

### 🤯 Challenges
- Escaping bugs in Jinja templates took time to trace.
- Early static templates interfered with dynamic rendering.
- Coordination of DB schema vs. doc fields required adjustments.
- Input validation improvements mid-way required refactoring.

### 🧠 Lessons Learned
- Dynamic over static templates reduces maintenance.
- Validate early using `parse_obj_as()` for consistent input models.
- Breakpoint logging helps diagnose pipeline bugs quickly.
- Use ordered trace to trace step-by-step logic and failures.

### 🔁 Improvement Areas
- Adopt snapshot-based unit testing for each tool.
- Auto-validate tool registry and manifest vs. implemented wrappers.
- Expand artifact schema documentation for easier onboarding.

### 💬 Team Feedback
- Strong alignment between UX, system design, and backend.
- Toolchain model is powerful and extendable.
- Adding default template fallback logic helped reduce friction.

### 🚀 Outcome
- WP18 delivered on all scope items.
- Clear runway for WP20 (Drive upload) and GPT handoff.
- System feels robust, maintainable, and ready to scale.