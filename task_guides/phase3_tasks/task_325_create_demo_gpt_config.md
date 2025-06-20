# 🤖 Task 325: Create Demo-Only Custom GPT Configuration

## 🧠 Context
To support safe, public-facing outreach and demos, we want a second version of the MyHealth Assistant GPT that only supports **demo workflows** — no real uploads or sessions. This avoids risk and simplifies onboarding.

Repo: `ai-delivery-sandbox`, Branch: `sandbox-curious-fox`

## 🎯 Goal
Create a clean, demo-only GPT configuration that:
- Uses `/load_demo` instead of `/upload`
- Supports `/ask_vector`, `/summary`, `/export`
- Removes `/session` and `/upload` from tool list

## 📦 Deliverables

### 1. GPT Config File
- Copy the current GPT config file (e.g., `docs/custom_gpt_setup.md`) to:
  - `project/demo_mode/demo_gpt_setup.md`
- Update:
  - Title (e.g., "MyHealth Assistant – Demo Mode")
  - Description (highlight safe demo-only flow)
  - System instructions to reflect only `/load_demo` as entry point
  - Tools/actions to include only:
    - `POST /load_demo`
    - `POST /ask_vector`
    - `GET /summary`
    - `GET /export`

### 2. OpenAPI Schema File
- Copy `docs/openapi.json` to `project/demo_mode/demo_openapi.json`
- Update:
  - Remove `/upload`, `/upload/sas`, `/upload/log`, `/session`, `/process`
  - Keep only the safe, read-only demo routes

### 3. Token Handling Plan
- Include note in the GPT setup file:
  - How to create a short-lived bearer token for the demo GPT
  - Where to set the token value in GPT tool config
  - Reminder to rotate token periodically or monitor usage

### 4. Create Demo Folder
- Create directory: `project/demo_mode/`
  - Store the two files above
  - Use this for any future demo-specific prompts, branding, or onboarding content

---

## 🧪 Done When
- A clean GPT config + openapi schema are saved in `project/demo_mode/`
- The demo GPT can be configured using those files
- Token is safely scoped and documented

Let Stewart know when it’s ready for review and testing before public publishing.