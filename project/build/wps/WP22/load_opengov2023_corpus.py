import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
import pdfplumber
from app.tools.tool_wrappers.loadCorpus import Tool

# Step 1: Download the PDF
doc_url = "https://publications.gc.ca/collections/collection_2024/sct-tbs/BT22-278-2023-eng.pdf"
pdf_path = "opengov2023.pdf"
response = requests.get(doc_url)
with open(pdf_path, "wb") as f:
    f.write(response.content)
print("✅ PDF downloaded")

# Step 2: Extract text from the PDF
with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
print(f"✅ Extracted {len(text)} characters from PDF")

# Step 3: Prepare and run loadCorpus
tool = Tool()
input_dict = {
    "file_contents": text,
    "file_name": "Open Government Guidebook 2023",
    "metadata": {
        "source": "GoC",
        "document_type": "Guidebook",
        "year": 2023
    }
}

result = tool.run_tool(input_dict)
print("✅ Corpus loaded:", result)