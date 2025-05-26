### Project Profile Versioning Design

#### 📌 Purpose
As project profiles become a dynamic part of the PolicyGPT memory and drafting system, versioning is needed to:
- Track changes to project context over time
- Support downstream artifact traceability
- Avoid accidental overwrites during iterative profiling

#### ✅ Default Behavior
- By default, all profiles are stored with a `version = 'v1'`
- Existing code assumes a single version and uses `project_id` as primary key

#### 🧠 Design Update
We introduce support for versioning using a `(project_id, version)` compound key.

##### Fields
```python
project_id: str       # unique identifier of the project
version: str = 'v1'   # version tag, e.g., v1, v2, or timestamped like 2024_05_25_1830
```

##### Syntax
- Simple semantic tags like `v1`, `v2`, `draft`, `final`
- Or datestamped strings for higher resolution

##### Retrieval Strategy
- If version is unspecified, default to `latest` (max version tag, assuming sortable)
- Add `load_latest_profile(project_id)` to the ProjectProfileEngine

##### Saving Strategy
- Option 1: Overwrite latest (backward-compatible)
- Option 2: Insert new row per version (future-proof, needs logic to resolve conflicts)

#### 🧪 Minimal Impact Strategy
To minimize refactoring, we:
- Keep default version = 'v1'
- Only add version support to API and DB when multiple versions are explicitly needed
- Backfill existing profiles with version = 'v1'

#### 🛠️ Next Steps
- Update schema and models to include version field (optional for now)
- Add logic to `load_latest_profile()`
- Flag version conflicts during save attempts

---
This prepares the system for evolving multi-version project needs while avoiding unnecessary disruption now.