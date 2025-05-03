## 🧱 MVP Stack and Component Design – GPT-First Architecture

### 1. 🧠 Custom GPT (Frontend)

#### ✅ Name: `CareerCoach-GPT`
#### ✅ System Prompt Scaffold:
```
You are CareerCoach, an AI mentor for kids aged 9–14. Your goal is to help them discover careers that match their interests, traits, and dreams using thoughtful questions and encouraging language.

Use the tools provided to:
- Load coaching prompts
- Retrieve career data
- Save or review reflections

Always respond in a warm, structured format with Markdown and emojis.
You NEVER guess answers. Use tools to retrieve knowledge or save data.
```

### 2. 🔧 OpenAPI Schema for Tools
```yaml
paths:
  /load_prompt:
    get:
      parameters: [prompt_id]
      responses: { 200: { content: CoachingPrompt } }

  /get_yaml_segment:
    get:
      parameters: [category]
      responses: { 200: { content: CareerSegment } }

  /save_reflection:
    post:
      requestBody: { session_id, career_id, text }
      responses: { 200: { success: boolean } }

  /fetch_summary:
    get:
      parameters: [session_id]
      responses: { 200: { summary: string } }
```

### 3. 🚀 FastAPI Backend

#### 🔌 Routes
- `GET /load_prompt`
- `GET /get_yaml_segment`
- `POST /save_reflection`
- `GET /fetch_summary`

#### 🧰 Utilities
- `yaml_parser.py`, `prompt_loader.py`, `notion_client.py`, `airtable_client.py`

### 4. 📦 Prompt Loader
- File-based JSON prompt templates per coaching journey

### 5. 💾 Memory
- Airtable or Notion API
- Linked by session ID, privacy-friendly, user-controlled

### 6. 📚 Knowledge Loader
- YAML segments from Git
- Schema-aligned, safe content for grounding GPT

### 📁 Component File List
```
app/
  main.py
  routes/
    prompts.py
    segments.py
    memory.py
  utils/
    yaml_parser.py
    prompt_loader.py
    airtable_client.py
    notion_client.py
  schemas/
    prompt.py
    segment.py
    reflection.py
  openapi.yaml
```

### 🧭 Mapped User Flows

#### 👧 Explorer:
- Chooses prompt → `/load_prompt`
- Answers Q&A → GPT
- Career match → `/get_yaml_segment`
- Reflects → `/save_reflection`

#### 👩‍👧 Supporter:
- Views summary → `/fetch_summary`

#### 🧑‍🏫 Spark:
- Shares GPT → QR code
- Aggregates → `/fetch_summary`
- Leads group reflection → GPT themes