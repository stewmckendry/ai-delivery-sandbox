# 📝 Task 326: Improve Human Readability of PDF Export

## 🧠 Context
The current `/export` route in the AI Health Records Assistant returns PDFs that are machine-generated but not user-friendly. The content appears as raw structured text without formatting or labeling, making it hard for patients, caregivers, or providers to read.

Repo: `ai-delivery-sandbox`, Branch: `sandbox-curious-fox`

## 🎯 Goal
Improve the formatting and presentation of exported PDFs so that they:
- Are easy to read and interpret for humans
- Include section headings, spacing, and readable fonts
- Optionally group content by clinical type or document type

## 📦 What to Update

### 1. PDF Generation
- Update the `/export` route logic to:
  - Add clear section headings (e.g., "Visit Notes", "Lab Results")
  - Format entries with spacing, indentation, and optional date labels
  - Use standard readable fonts (e.g., Helvetica, 11pt)
- You may continue to use the `reportlab` or `fpdf` Python libraries
- Keep to plaintext input + formatting — **do not embed binary assets** to avoid Git conflicts

### 2. File Naming
- Exported PDF filename should include readable session or source reference:
  - Example: `health_summary_<session_key>.pdf`

## ✅ Constraints
- Do **not** include binary files (PDFs) in PRs — code-only changes only
- Output must remain compatible with existing blob upload logic

## 🧪 Done When
- Exported PDFs are visually structured and clear for review
- Output file names are clean and user-meaningful
- No binary files added to Git

Let Stewart know when this is complete so it can be reviewed and tested with demo flows.