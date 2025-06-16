# Task 202: Operator Prompt Templates

## 🎯 Goal
Guide users to gather the right health data from portals via OpenAI Operator using prompt templates.

## 📂 Context
This is part of Phase 2 - refer to phase2_operator_architecture.md for overall architecture.  We are replacing the portal scraping with OpenAI Operator to streamline data retrieval.

## 📂 Target Files
- `project/prompts/operator_templates.md` (new)
- `project/docs/operator_guidance.md` (new)

## 📋 Instructions
- Draft 3–5 reusable Operator prompts:
  - Visit Summary (e.g. login, go to Visits, download PDF)
  - Lab Results
  - Billing Info
  - All records (if needed)
- Include guidance for the user:
  - Download format preference (PDF/HTML)
  - Naming convention: portal_date_type.pdf
  - Return to Copilot after download

## 🧪 Test
- Copy-paste prompt into Operator
- Ensure it leads to target file type
- User downloads and names file properly

## ✅ What to Report Back
- Final prompts
- Screenshot or logs showing operator steps
- Files generated

This enables Copilot to give users strong, task-specific prompts for Operator navigation.