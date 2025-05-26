## 📥 Steps to Ingest GoC Document with `loadCorpus`

This guide describes how to ingest a Government of Canada policy document into the embedded corpus for WP22 testing.

---

### 📄 Sample Document
- **Title**: *Open Government Guidebook 2023*
- **URL**: https://publications.gc.ca/collections/collection_2024/sct-tbs/BT22-278-2023-eng.pdf

---

### 🧰 Requirements
- Python environment with PolicyGPT setup
- `loadCorpus.py` in `app/tools/tool_wrappers`
- PDF-to-text converter (e.g., `pdfplumber`, `PyMuPDF`, or online tool)

---

### 🪜 Ingestion Steps

1. **Download the PDF**
```bash
curl -o opengov2023.pdf "https://publications.gc.ca/collections/collection_2024/sct-tbs/BT22-278-2023-eng.pdf"
```

2. **Extract Text Content** (example using `pdfplumber`)
```python
import pdfplumber

with pdfplumber.open("opengov2023.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

with open("opengov2023.txt", "w") as f:
    f.write(text)
```

3. **Prepare the Input Dictionary**
```python
from app.tools.tool_wrappers.loadCorpus import Tool

tool = Tool()
with open("opengov2023.txt") as f:
    file_contents = f.read()

input_dict = {
    "file_contents": file_contents,
    "file_name": "Open Government Guidebook 2023",
    "metadata": {
        "source": "GoC",
        "document_type": "Guidebook",
        "year": 2023
    }
}
```

4. **Run the Tool**
```python
result = tool.run_tool(input_dict)
print(result)
```

---

### ✅ Output
- Indexed content into Chroma DB
- Summary and trace log generated
- Can now be queried via `queryCorpus.py`

---

For any ingestion issues, check `CHROMA_DIR` and logging output for troubleshooting.