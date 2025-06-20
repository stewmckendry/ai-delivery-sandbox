# User Access & Usage Guidance

This guide explains how to try the AI Health Records Assistant safely.
It covers who can use the assistant, when to rely on OpenAI Operator, and
how to test features without sharing personal information.

## Who Can Use the Assistant?
- **ChatGPT Pro users** have full access, including the Operator tool for
  navigating portals.
- **Plus and free-tier users** can still chat with the assistant and upload
  files, but Operator is unavailable.

## When to Use Operator
- Use Operator when retrieving records from **your own health portals**.
  It keeps the browser session private and lets you confirm each step.
- For testing or demo flows, Operator is **not required**. You can upload
  sample files or use the `/load_demo` endpoint to load mock records.

## What Works Without Pro
- Upload mock PDFs from `project/demo_data` or your own test files.
- Ask questions about these demo sessions using `/ask_vector` or `/summary`.
- Export structured content and review logs even without Operator.

## Demo Version
The demo version lets you explore the assistant without uploading any personal health data.
Use the `/load_demo` endpoint or the sample PDFs in `project/demo_data` to create a
session populated with mock records. You can ask questions, practice generating
summaries, and experiment with PDF exports or log review. The goal is to show what the
assistant can do before linking your own portals or sensitive files.

## Best Practices for Real Portals
- Only use portals you personally have access to.
- Review your portal's terms of use before automating downloads.
- Keep downloads secure and delete them when finished.
- Remember the assistant is a **proof of concept** and may contain bugs.

## Disclaimer
MyHealth Assistant is an early-stage proof of concept that helps you gather,
organize, and explore your own health records. It is designed for informational
and educational purposes only.

- **Not a medical device.** The Assistant does not diagnose conditions, provide
  medical advice, or replace consultation with a qualified clinician.
- **No clinical decision support.** Summaries and answers come from analyzing
  your uploaded documents; they should be reviewed with a healthcare professional
  before you rely on them.
- **Use with care.** The tool is still under active development and may contain
  bugs or incomplete features. We recommend using test data or proceeding at
  your own risk.

Always double-check results and consult your healthcare provider for questions
about your treatment or diagnosis.
