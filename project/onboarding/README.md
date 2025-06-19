# Onboarding Guide: MyHealth Copilot

Welcome to the MyHealth Copilot sandbox! This folder gathers quick links and snippets so you can test the assistant with demo data and understand how to use it safely.

## Quick Start
1. [Generate a short-lived token](../../README.md#setup) and start the API (`run_local.sh` or Docker).
2. Call the `/load_demo` endpoint to create a new session preloaded with a sample PDF:

```bash
TOKEN=<your token>
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  https://ai-delivery-sandbox-production-d1a7.up.railway.app/load_demo
```

The response contains `session_key`, `source`, and `source_url`. Use the key to fetch summaries:

```bash
curl "https://ai-delivery-sandbox-production-d1a7.up.railway.app/summary?session_key=<key>" \
  -H "Authorization: Bearer $TOKEN"
```
- Demo PDF files used by `/load_demo` live in [`project/demo_data`](../demo_data).

## GPT Starter Prompts
See [`prompt_starter_kit.md`](../docs/prompt_starter_kit.md) for example questions like *"What medication was prescribed in the demo visit?"*.

## Safe Usage
- Read the [Disclaimer](../docs/disclaimer.md) before relying on any outputs.
- Review [User Access Guidance](../docs/user_access_guidance.md) for who can use Operator and when.
- Advanced users can follow the [Operator Guidance](../docs/operator_guidance.md) to download their own records.

## Demo Session Snippet
Below is a short session snippet the GPT can preload:

```
POST /load_demo -> {"session_key": "sess123", "source": "family_doctor_visit.pdf"}
Then ask: "Summarize why the patient saw the doctor on 2023‑02‑20."
```

Use this as a template when sharing the assistant or writing guides.

---
For more details about the API, inspect [`docs/openapi.json`](../../docs/openapi.json).
