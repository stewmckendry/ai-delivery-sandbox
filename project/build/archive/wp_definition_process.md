### 📦 Work Package Definition Process – Finalized

---

#### 🔧 Step-by-Step Workflow

**Step 1: Select Work Package**
- **Responsibility:** Human Lead
- **Action:** Choose WP to begin from `work_package_overview.md`

**Step 2: Draft WP Definition (Canvas)**
- **Responsibility:** GPT
- **Template Output:**

```markdown
## WP ID: WPx
## WP Name: <name>

### 🎯 Outcome
By the end of this WP, as a <user/system>, I will be able to <X,Y> which supports benefits <A,B,C>.

### 🧭 Scope
**In Scope:**
- <What this WP covers>

**Out of Scope:**
- <Exclusions or deferments>

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `...`     | ...         |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WPx/WPx_design.md` | Design plans |
| `project/build/wps/WPx/WPx_deployment.md` | Deployment instructions |
| etc. |

### ✅ Acceptance Criteria
- [ ] <List of criteria defining “done”>

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1      | Plan and clarify scope using referenced design docs |
| T2      | Implement `X` module |
| T3      | Unit test `X` with cases A, B, C |
| T4      | Deploy to dev/test |
| T5      | Validate acceptance criteria met |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `system_design/foo.md` | Data schema |
| `discovery/bar.md`     | User journey |

### 📝 Notes to Development Team
- Clarify assumptions or special considerations
```

**Step 3: Review with Human Lead**
- **Responsibility:** Human Lead

**Step 4: Commit to Git**
- **Responsibility:** GPT
- **Location:** `project/build/wps/WPx/WPx_definition.md`

**Step 5: Cross-check WP Overview**
- **Responsibility:** GPT

---

### 🔁 Iteration Plan
- One WP per commit and review loop
- Chunk long files if needed to bypass commit/fetch limits

---

### 📌 Division of Responsibility

| Task | GPT | Human |
|------|-----|-------|
| Extract WP from overview | ✅ |  |
| Generate WP draft | ✅ |  |
| Review/edit WP draft |  | ✅ |
| Commit to Git | ✅ |  |
| Resolve doc ambiguities |  | ✅ |
| Final completeness check | ✅ | ✅ |