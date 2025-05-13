# 🧬 Schema Template – Best Practice

## 📌 Overview
Explain the schema’s purpose, how it maps to the user journey or reporting, and how it is validated.

- **Purpose:** e.g., logs structured symptom data for export
- **Used In Tools:** list tool routes that read/write this schema
- **Export Table:** e.g., `symptom_log_export`

## 🧾 Field Definitions
| Field             | Type       | Description                              | Source                     |
|------------------|------------|------------------------------------------|----------------------------|
| `user_id`         | string     | Unique identifier                        | session / auth layer       |
| `symptoms`        | list[str]  | List of symptom IDs                      | YAML map                   |
| `timestamp`       | datetime   | Time of logging                          | UTC default                |
| `log_metadata`    | dict       | Additional context info                  | tool-level enrichment      |

## ✅ Validation Rules
- Enum checks (e.g., symptom IDs exist in YAML)
- Format constraints (ISO datetime, UUIDs)
- Optional fields that default to null

## 📤 Export Mapping
- How this model is serialized and sent to SQL, PDF, or FHIR
- Any joins or enrichments performed pre-export

## 🔁 Versioning
- Describe changes from v1 → v2 if applicable
- How backward compatibility is handled

---
Include links to YAML sources, export views, and tool validators.