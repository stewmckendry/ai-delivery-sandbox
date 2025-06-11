# Codex Agent Task: YAML Prompt Loader

## 🎯 Goal
Create a utility that loads YAML prompt templates and renders them with variables.

## 📂 Target File
`app/prompts/loader.py`

## 📋 Instructions
- Load a YAML file from `app/prompts/*.yaml`
- Parse the YAML into a dict with `template` and optional metadata
- Use a dictionary of variables to render the `template` string
- Return the rendered prompt

## 📄 Example YAML
```yaml
name: summarize_lab_results
template: |
  Summarize the following lab results:
  {{ lab_data }}
```

## ✅ What to Report Back
- File path and function code
- Example YAML + variable dict + rendered output
- Assumptions or limitations (e.g., templating syntax)
- Any helper libraries used (like `jinja2`)

Refer to [review_checklist.md](review_checklist.md) for formatting.