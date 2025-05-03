## ⚙️ Scaffold: FastAPI Routes + GPT Tools + System Prompt

---

### 🛠 FastAPI Route Handlers

#### 📄 `routes/prompts.py`
```python
from fastapi import APIRouter, HTTPException
from utils.prompt_loader import load_prompt

router = APIRouter()

@router.get("/load_prompt")
def load_prompt_route(prompt_id: str):
    try:
        return load_prompt(prompt_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
```

#### 📄 `routes/segments.py`
```python
from fastapi import APIRouter, HTTPException
from utils.yaml_loader import load_yaml_segment

router = APIRouter()

@router.get("/get_yaml_segment")
def get_yaml_segment_route(category: str):
    try:
        return load_yaml_segment(category)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
```

#### 📄 `routes/memory.py`
```python
from fastapi import APIRouter, Request
from utils.memory_manager import MemoryManager

router = APIRouter()
memory = MemoryManager()

@router.post("/save_reflection")
def save_reflection(data: dict):
    memory.save_reflection(**data)
    return {"success": True}

@router.get("/fetch_summary")
def fetch_summary(session_id: str):
    return memory.fetch_summary(session_id)
```

---

### 📐 OpenAPI Tools Schema (for Custom GPT)
```yaml
openapi: 3.0.0
info:
  title: CareerCoach Tool API
  version: 1.0.0
paths:
  /load_prompt:
    get:
      parameters:
        - in: query
          name: prompt_id
          required: true
          schema: { type: string }
      responses:
        200:
          description: Coaching prompt

  /get_yaml_segment:
    get:
      parameters:
        - in: query
          name: category
          required: true
          schema: { type: string }
      responses:
        200:
          description: Career segment JSON

  /save_reflection:
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                session_id: { type: string }
                career_id: { type: string }
                prompt_id: { type: string }
                text: { type: string }
      responses:
        200: { description: Acknowledged }

  /fetch_summary:
    get:
      parameters:
        - in: query
          name: session_id
          required: true
          schema: { type: string }
      responses:
        200:
          description: Summary data
```

---

### 🧠 CareerCoach Custom GPT System Prompt
```
You are CareerCoach, an AI mentor for kids aged 9–14. Your job is to help them explore fun, creative, and meaningful careers using engaging questions and grounded answers.

🛠 Tools Available:
- /load_prompt to fetch coaching flows
- /get_yaml_segment to find career ideas
- /save_reflection to log thoughts
- /fetch_summary to review a session

Always explain career suggestions using metaphors and emojis. Invite reflection. Never guess — use tools.
```