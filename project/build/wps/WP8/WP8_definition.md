## WP ID: WP8
## WP Name: Evidence and Citation Tool

### 🌟 Outcome
By the end of this WP, as a **policy drafter or approver**, I will be able to automatically insert, trace, and review citations used in generating or validating gate documents. This ensures traceability, transparency, and defensibility of all LLM-generated content.

### 🧽 Scope
**In Scope:**
- Lookup relevant evidence from indexed content
- Log evidence sources and insert citation markers
- Generate and display a citation index
- Log source reliability and timestamps

**Out of Scope:**
- External web search (WP14)
- Manual citation editing interface (future UI WP)

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/citation_inserter.py` | Injects citation markers into draft text |
| `app/tools/evidence_lookup.py` | Searches indexed evidence related to prompt or section |
| `app/tools/evidence_logger.py` | Stores metadata about used sources |
| `app/tools/generate_citation_index.py` | Assembles list of all citations for export |
| `app/db/models/EvidenceCitation.py` | Captures link between draft content and source |
| `app/db/models/CitationSource.py` | Metadata about citation sources |
| `app/db/models/EvidenceIndex.py` | Local index of pre-approved reference materials |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP8/WP8_evidence_tool_flow.md` | Diagram of how evidence is searched, cited, and logged |
| `project/build/wps/WP8/WP8_citation_index_template.md` | Example export of final citation index format |

### ✅ Acceptance Criteria
- [ ] Drafts contain inline citation markers from `evidence_lookup`
- [ ] All sources are logged with metadata (timestamp, trust score, etc.)
- [ ] A citation index can be exported alongside the final document
- [ ] Feedback flow logs unused or broken citations for cleanup

### 🛠 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Build `evidence_lookup.py` to return relevant excerpts from `EvidenceIndex` |
| T2 | Inject citations using `citation_inserter.py` |
| T3 | Create logger and DB models for source tracking |
| T4 | Build `generate_citation_index.py` for export and review |
| T5 | Integrate with planner toolchain (via WP3a) and validation layer (WP4) |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `acceptance_criteria_v2.md` | References to traceability and source transparency |
| `tool_catalog_v2.md` | Describes citation tools and functions |
| `session_memory_model_v2.md` | Where citations live in mid-term memory |

### 📝 Notes to Development Team
- The tool should be planner-compatible (exposed via tool registry, wrapped with logs)
- Designed for proactive AND reactive citation capture
- Must support export with rendered markdown + source list

### 🧠 Clarifications
- 🔍 **Proactive integration:** Planner in WP3a calls `evidence_lookup.py` during document generation to pull supporting materials *before* drafting.
- 🏗 **Reactive integration:** `validate_section.py` (WP4) may use evidence tools to backfill or verify claims post-generation.
- 📚 **Citation Index** is exportable as a markdown table for inclusion in final documents.