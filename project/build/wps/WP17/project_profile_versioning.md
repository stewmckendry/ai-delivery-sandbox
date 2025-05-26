## Project Profile Versioning Design Note

### 🎯 Purpose
Support future ability to track changes over time in the project profile, while maintaining the current simple upsert model.

### 🧱 Design Overview
- Each profile version is uniquely identified by a `(project_id, version)` pair.
- `version` is a string field, defaulting to `'v1'`, and incremented manually or programmatically.
- A composite primary key is created over `(project_id, version)`.

### 🛠 Table Schema (optional future update)
```sql
CREATE TABLE project_profile (
    project_id TEXT,
    version TEXT DEFAULT 'v1',
    title TEXT NOT NULL,
    sponsor TEXT,
    ... (other fields) ...
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (project_id, version)
);
```

### 📋 Implementation Plan
- Add `version` field to model and DB table.
- Maintain current behavior by always loading and updating `version = 'v1'` unless otherwise specified.
- Allow newer versions to be inserted explicitly if versioning is enabled.

### 🔧 Minimal Impact Strategy
- Backward compatible: `version` is optional in logic.
- Extend `load_profile` to retrieve latest by `last_updated` if multiple versions exist.
- Update `save_profile` to increment version or clone on demand.

### 🧪 Future Work
- Add history viewer in GPT UX.
- Add `project_profile_log` table for full audit trail if needed.

### 🤝 Coordination
- Does not impact current functionality.
- Can be adopted incrementally by WP7 or a future work package.