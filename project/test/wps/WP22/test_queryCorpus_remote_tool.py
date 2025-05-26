import os
import requests
import pdfplumber
from app.tools.tool_wrappers.loadCorpus import Tool as LoadTool
from app.tools.tool_wrappers.queryCorpus import Tool as QueryTool

# Ensure environment is configured for remote
os.environ["CHROMA_SERVER_HOST"] = "your-remote-host"
os.environ["CHROMA_SERVER_HTTP_PORT"] = "8000"
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Load corpus into remote Chroma using GitHub-hosted PDF
raw_url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/test/wps/WP22/opengov2023.pdf"
pdf_path = "opengov2023.pdf"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(raw_url, headers=headers)
with open(pdf_path, "wb") as f:
    f.write(response.content)

with open(pdf_path, "rb") as f:
    if f.read(4) != b"%PDF":
        raise ValueError("Invalid PDF format")

with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

load_tool = LoadTool()
load_tool.run_tool({
    "file_contents": text,
    "file_name": "Open Government Guidebook 2023",
    "metadata": {"source": "GoC", "year": 2023}
})

# Run remote query tests
query_tool = QueryTool()
tests = [
    {"name": "R1 - Open government policy objectives", "query": "open government policy objectives"},
    {"name": "R2 - Transparency and digital services", "query": "transparency and digital services"},
]

for test in tests:
    print(f"\n🔹 {test['name']}")
    result = query_tool.run_tool({"query": test["query"]})
    print(result["answer"])
    print("---")