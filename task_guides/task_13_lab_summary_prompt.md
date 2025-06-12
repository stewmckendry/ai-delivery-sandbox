# Codex Agent Task: Lab Results Summarizer Prompt

## 🎯 Goal
Generate a readable health summary from structured lab results using OpenAI and a YAML prompt template.

## 📂 Target File
- `app/prompts/summarizer.py`

## 📋 Instructions
- Load the `summarize_lab_results.yaml` template from `app/prompts/`
- Accept list of `LabResult` dicts as input
- Render the template into a string using field substitution
- Use `openai.ChatCompletion.create` to submit the prompt
- Return the natural-language summary text

## 🧪 Test
- Add `tests/test_summarizer.py`
- Mock OpenAI call and test correct summary output from known lab input

## 🔄 Reuse
- Use `app.prompts.loader` to render templates
- Use `openai` from `requirements.txt`

## ✅ What to Report Back
- Summary-generating function and unit test
- Example output summary string
- Notes on any assumptions or formatting challenges

Refer to `task_guides/review_checklist.md` for structure.