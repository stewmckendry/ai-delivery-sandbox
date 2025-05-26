import requests
import sys
import os
import pdfplumber

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))
print("📂 Project root added to sys.path:", sys.path)
from app.tools.tool_wrappers.loadCorpus import Tool

# Step 1: Download the PDF with headers (SKIP as downloaded manually)
"""
doc_url = "https://publications.gc.ca/collections/collection_2024/sct-tbs/BT22-278-2023-eng.pdf"
pdf_path = "opengov2023.pdf"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(doc_url, headers=headers)
with open(pdf_path, "wb") as f:
    f.write(response.content)
print("✅ PDF downloaded")
"""

# Step 2: Validate the PDF format
pdf_path = "opengov2023.pdf"
with open(pdf_path, "rb") as f:
    magic = f.read(4)
    if magic != b"%PDF":
        raise ValueError("Downloaded file is not a valid PDF. Got header: " + str(magic))
print("✅ File format validated: PDF")

# Step 3: Extract text
with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
print(f"✅ Extracted {len(text)} characters from PDF")

# Step 4: Run loadCorpus
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