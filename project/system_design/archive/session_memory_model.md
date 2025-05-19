---

## title: Session Memory Model

## Overview

This document defines how memory is scoped, structured, and managed across PolicyGPT user sessions. It includes session lifecycle phases, data models, caching strategies, fallback rules, and interfaces between GPT agents, FastAPI endpoints, and storage systems.

---

## Memory Scope Layers

| Layer        | Duration       | Contents                                                             | Used For                              |
|--------------|----------------|----------------------------------------------------------------------|----------------------------------------|
| Short-Term   | One GPT exchange | Latest prompt + tool response                                         | Immediate tool chaining + context      |
| Mid-Term     | Session duration | Project YAML, current section state, input mappings                  | Draft generation, validation           |
| Long-Term    | Persistent      | Full document history, approval metadata, tool logs                  | Versioning, audit trail, re-ingestion  |

---

## Lifecycle Stages

| Phase            | What is Stored                                | Where Stored                  | Accessed By              |
|------------------|-----------------------------------------------|-------------------------------|---------------------------|
| Start Session    | New session ID, project profile stub           | PostgreSQL + YAML in Drive    | GPT + FastAPI             |
| Upload Inputs    | File metadata, extracted content               | PostgreSQL + GDrive           | GPT tools                 |
| Draft Section    | Section content, source mapping, prompts used | PostgreSQL + YAML snapshot    | GPT + Composer tool       |
| Revise Section   | Revisions log, source diffs                   | PostgreSQL                    | GPT + Revision engine     |
| Commit Artifact  | Final output, reviewers, approvals             | GDrive + PostgreSQL + Audit   | GPT + User Review         |

---

## Implementation Model

### Data Schema (PostgreSQL + YAML Hybrid)

**project_profile.yaml**
```yaml
project_id: abc123
project_title: Building Accessibility Upgrade
gate_stage: Gate 1
stakeholders:
  - name: Finance
    role: Reviewer
key_risks:
  - Risk of delayed procurement
strategic_alignment:
  - National Infrastructure Plan 2024
```

**PostgreSQL Tables**
```sql
CREATE TABLE SessionState (
    session_id TEXT PRIMARY KEY,
    user_id TEXT,
    project_id TEXT,
    yaml_state JSONB,
    last_active TIMESTAMP
);

CREATE TABLE SectionDraft (
    id SERIAL PRIMARY KEY,
    project_id TEXT,
    section_id TEXT,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP
);
```

**Access Patterns**
- YAML is used for cross-session shared context.
- PostgreSQL is used for live drafts, logs, and transactions.
- GDrive stores versioned snapshots of full artifacts.

---

## Example Session Flow

### User: "Generate Gate 0 Summary"
1. **Start session** → session ID created, empty YAML stub stored
2. **Upload interview notes** → parsed and cached under session, references YAML state
3. **Draft "Rationale" section** → section generated, source citations logged
4. **Revise with feedback** → tool logs edits, updates PostgreSQL, and rewrites YAML
5. **Commit section** → metadata versioned, Google Drive link stored, YAML locked

---

## FastAPI Scaffold (Session Storage & Memory)

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .db import get_db
from .models import SessionState

router = APIRouter()

@router.post("/start_session")
def start_session(user_id: str, project_id: str, db: Session = Depends(get_db)):
    session_id = uuid4().hex
    default_yaml = {...}  # Minimal YAML stub
    db_session = SessionState(
        session_id=session_id,
        user_id=user_id,
        project_id=project_id,
        yaml_state=default_yaml,
        last_active=datetime.utcnow()
    )
    db.add(db_session)
    db.commit()
    return {"session_id": session_id}
```

---

## Risk Table and Mitigations

| Risk                            | Mitigation                                                              |
|---------------------------------|--------------------------------------------------------------------------|
| Multi-user conflict             | Session isolation via unique `session_id`, scoped DB row + YAML file    |
| Stateless GPT response          | Embed YAML + prompt memory into system message for continuity           |
| Drive write fail                | Cache YAML + metadata until Drive confirms write                        |
| Stale context from old version | Timestamp compare and YAML re-merge checks                              |

---

## Logging and Audit

- Session start/close: `SessionLog`
- YAML snapshot saves: `AuditTrail`
- Tool interaction: `PromptLog`, `ToolLog`
- Commit events: `AuditTrail`, `Drive metadata`

**Log Schemas:**
- `SessionLog`: session_id, user_id, start_time, end_time
- `PromptLog`: prompt_id, session_id, tool_name, input_payload, timestamp
- `ToolLog`: tool_name, session_id, output_payload, status_code, latency
- `AuditTrail`: event_id, session_id, user_id, artifact_id, action_type, timestamp, metadata

---

## Unknowns, Constraints, and Mitigations

| Constraint                            | Mitigation Plan                                                                 |
|---------------------------------------|---------------------------------------------------------------------------------|
| Concurrent edits to same artifact     | Lock per section on edit start; serialize writes                               |
| Session expiry (e.g., timeout)        | Auto-recover via project ID and YAML versioning                                |
| GPT memory limits (e.g., >10k tokens) | Use project YAML to feed prior context incrementally + token estimator tools   |
| Loss of DB session                    | Rehydrate from latest YAML snapshot or Drive file metadata                     |

---

## Alignment with System Design Docs

- **Tool Catalog**: Tools read/write from `SessionState`, `SectionDraft`, and YAML files. Composer tool uses YAML to conditionally call Draft/Revise/Commit logic.
- **DB Schema Notes**: `SessionState`, `SectionDraft`, `AuditTrail`, and `ToolLog` tables directly reflect session activity.
- **User Journeys**: All Journey A/B/C segments use scoped sessions to persist inputs, edits, and state transitions.
- **Integration Points**: YAML schema is the core shared context exchanged across GPT ↔ FastAPI ↔ Drive ↔ DB systems.
- **Error Handling Matrix**: Session context is used to interpret, retry, or rollback tool actions after error events.

---
