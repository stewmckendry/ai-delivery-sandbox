## 🔁 Addendum: Feature Delivery Rhythm

This document defines the step-by-step mold for delivering features during the Build Phase. It reflects best practices from Feature 6 and is intended to be reused by all pods.

---

### 🔧 Standard Rhythm for Each Feature

#### 1. **Plan**
- Create a task via `task_lifecycle.create`
- Write and commit the high-level plan to `project/delivery/features/<feature>/plan.md`
- Define a task list to track progress and commit to `task_list.md`

#### 2. **Design**
- Write a detailed design spec and commit to `design.md`
- Include:
  - Upstream and downstream tool flows
  - Input/output schemas
  - Alignment to app_features and user_app_flows
  - Assumptions and builder guidance
- Log thoughts via `chain_of_thought.append`

#### 3. **Design Addenda (if needed)**
- As understanding evolves, write separate clarifying docs (e.g., `schema_notes.md`, `logic_notes.md`)
- Commit them alongside the design

#### 4. **Build**
- Implement code in `app/` and models in `app/models/`
- Add unit tests in `app/engines/test_*.py` or `test/`
- Commit iteratively after each piece

#### 5. **Validate**
- Use or extend `schema_validator.py` to lint YAMLs
- Run tests manually or via `pytest`
- Wire into CI if needed

#### 6. **Log & Communicate**
- Log thoughts after each phase with `chain_of_thought`
- Update and recommit `task_list.md` after each step
- Track any follow-up needed in other features (e.g., symptoms scoring in FA2)

---

### 📁 Folder Conventions
- `project/delivery/features/<feature_id>/`
  - `plan.md`, `design.md`, `task_list.md`, `schema_notes.md`, etc.
- `app/engines/`, `app/models/` → All engines and data models
- `reference/` → Static YAMLs validated by engines

---

### ✅ Principles
- **Persist as you go** – commit plan, design, and decisions early
- **Log your thoughts** – for transparency and handoff
- **Traceability** – every output must trace to prior inputs (features → design → code → test)
- **Minimize friction** – design for fast iteration and clarity
- **Own and share the rhythm** – it’s the core of high trust, low drag delivery

---