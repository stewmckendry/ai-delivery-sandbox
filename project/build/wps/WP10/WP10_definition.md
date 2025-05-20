## WP ID: WP10
## WP Name: Export and Translation Layer

### 🌟 Outcome
By the end of this WP, as a **policy team member**, I will be able to export finalized documents into a standardized gate submission package, including both original and translated versions. This supports the benefit of **official submission readiness**, **compliance with bilingual requirements**, and **ease of distribution**.

### 🧽 Scope
**In Scope:**
- Export to structured file format (PDF/Markdown/ZIP)
- Apply consistent layout and filename conventions
- Organize outputs by Gate # and timestamp in Google Drive
- Dual-language (English + French) translation export

**Out of Scope:**
- External drive integrations beyond Google Drive (future WP)
- Custom layout styling beyond provided templates

### 📦 Deliverables
| File Path | Description |
|-----------|-------------|
| `app/tools/export_to_gate_package.py` | Assembles document into official gate package format |
| `app/tools/translate_to_official_language.py` | Translates full document into bilingual format (a.k.a. `dual_language_exporter.py`) |

### 📄 Supporting Documentation (to generate)
| File Path | Description |
|-----------|-------------|
| `project/build/wps/WP10/WP10_export_formats.md` | Layout and format examples for export package |
| `project/build/wps/WP10/WP10_translation_rules.md` | Handling of translation, e.g., section labels, citations, placeholders |

### ✅ Acceptance Criteria
- [ ] Gate package includes all sections, metadata, and citations
- [ ] Exported format is compliant with gate submission expectations
- [ ] Folder in Google Drive is organized by gate # and timestamp
- [ ] Translated version matches section structure and retains citations

### 💪 Tasks
| Task ID | Description |
|---------|-------------|
| T1 | Build `export_to_gate_package.py` with folder + layout logic |
| T2 | Integrate metadata + section content into export logic |
| T3 | Build `translate_to_official_language.py` for dual language export |
| T4 | Write format and translation rules docs |
| T5 | Add export tool to planner toolchain (WP3a) and test end-to-end |

### 📚 Reference Documentation
| File Path | Usage |
|-----------|--------|
| `gate_reference_v2.yaml` | Defines gate structure and expected submission contents |
| `tool_catalog_v2.md` | Tool capabilities for export and translation |
| `acceptance_criteria_v2.md` | Compliance checks for export output |

### 📝 Notes to Development Team
- File naming convention: `Gate<Number>_YYYYMMDD_<DocName>.md/pdf`
- Ensure translation uses consistent terminology from `gate_reference.yaml`
- Use existing Google Drive toolchain for output destination

### 🧠 Clarifications
- 📄 Exporter handles **document assembly, formatting, and saving** to Drive
- 🌐 Translations target **bilingual policy submission** and are applied after draft finalization
- 🧲 Output folders should be grouped by gate to streamline committee review