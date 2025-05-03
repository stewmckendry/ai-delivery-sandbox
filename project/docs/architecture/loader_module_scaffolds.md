## 📦 YAML and Prompt Loader Module Scaffolds

### 📄 `yaml_loader.py`
```python
# utils/yaml_loader.py

import yaml
import os

def load_yaml_segment(category: str) -> dict:
    filename = f"project/inputs/knowledgebooks/segments/youth_career_guide_{category.lower()}.yaml"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"YAML file not found: {filename}")
    with open(filename, "r") as f:
        return yaml.safe_load(f)
```

---

### 📄 `prompt_loader.py`
```python
# utils/prompt_loader.py

import json
import os

def load_prompt(prompt_id: str) -> dict:
    filename = f"project/inputs/prompts/{prompt_id}.json"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Prompt not found: {filename}")
    with open(filename, "r") as f:
        return json.load(f)
```

---

### ✅ Purpose
- Modular loading of prompt templates and career knowledge segments
- Aligns with FastAPI route structure and tool interface
- Easy to test and replace as we grow the knowledgebook