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

## Best Practices for Real Portals
- Only use portals you personally have access to.
- Review your portal's terms of use before automating downloads.
- Keep downloads secure and delete them when finished.
- Remember the assistant is a **proof of concept** and may contain bugs.

## Disclaimer
See [disclaimer.md](disclaimer.md) for important limitations. The
assistant is not a medical device or clinical decision tool.
Use it at your own risk and verify all outputs.
