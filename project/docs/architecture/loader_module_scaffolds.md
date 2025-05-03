## 📦 YAML and Prompt Loader Module Scaffolds (Updated for Cloud)

### 📄 `yaml_loader.py`
```python
# utils/yaml_loader.py

import yaml
import requests

def load_yaml_segment(category: str) -> dict:
    url = f"https://raw.githubusercontent.com/<org>/<repo>/main/project/inputs/knowledgebooks/segments/youth_career_guide_{category.lower()}.yaml"
    response = requests.get(url)
    response.raise_for_status()
    return yaml.safe_load(response.text)
```

### 📄 `prompt_loader.py`
```python
# utils/prompt_loader.py

import json
import requests

def load_prompt(prompt_id: str) -> dict:
    url = f"https://raw.githubusercontent.com/<org>/<repo>/main/project/inputs/prompts/{prompt_id}.json"
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)
```

### ✅ Deployment-Ready Design
- Uses raw GitHub URLs
- YAML and JSON parsed safely
- Swappable to S3/CDN later with same interface

### 🗃 Git as Source of Truth
- Reference files (YAML/JSON) are version-controlled in Git
- Commits trigger updates to public URLs
- GitHub + raw URLs = transparent, inspectable data
- Aligns with ai-delivery-framework principles: traceability, reproducibility, observability