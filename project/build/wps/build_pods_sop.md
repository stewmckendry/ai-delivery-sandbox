## 🧭 Build Pods Standard Operating Procedure (SOP)

This SOP outlines the coordination rules and responsibilities for all Work Package (WP) Pods and the Lead Pod.

### 🎬 Activation of WP Pods
- **Initiator:** Lead Pod (via Human Lead)
- **Trigger:** Approved WP definition
- **Method:** Use `pod_message.md` template to deliver:
  - WP context and scope
  - Repo and branch info
  - Reference files
  - Expectations and SOP link

### 🔄 WP Pod Responsibilities
- **Execution:** Follow WP scope and deliverables
- **Documentation:** Update supporting docs listed in WP
- **Progress Updates:** Notify Lead Pod at:
  - Kickoff
  - Midpoint (progress + blockers)
  - Completion (link to deliverables + summary)
- **Blockers:** Raise immediately via Lead Pod, with:
  - Issue description
  - Affected deliverable or task
  - Suggested workaround (if any)
- **Minor Changes:** Pods can autonomously:
  - Adjust task ordering
  - Add minor clarifications to spec
  - Refactor implementation details without changing external behavior
- **Major Changes:** Must raise to Lead Pod if:
  - Scope creep occurs
  - Deliverables need to change
  - Dependencies shift

### 🔁 Design Feedback Loop (WP12)
- Trigger when implementation diverges from spec
- Share evidence: logs, diffs, updated implementation
- Use WP12 format to document patch
- Notify Lead Pod with summary

### 🧩 Lead Pod Responsibilities
- Track WP status, assignments, and updates
- Maintain `work_package_tracker.md`
- Review WP Pod updates, blockers, change requests
- Coordinate with WP12 for feedback loop
- Communicate shared changes across Pods
- Ensure cohesion across toolchain and architecture
- Handle escalations and prioritization

### 📚 References
- `project/build/work_package_tracker.md`
- `project/build/wps/pod_message.md`
- `project/build/wps/WP12_definition.md`

### 🤝 Collaboration Principles
- Respect defined scope but allow implementation flexibility
- Prioritize communication over assumption
- Escalate fast, resolve collaboratively
- Build for traceability and transparency