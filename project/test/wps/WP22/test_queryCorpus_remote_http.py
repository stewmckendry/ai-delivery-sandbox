import requests
import pdfplumber

# Remote endpoints
RAILWAY_BASE = "https://robust-adventure-production.up.railway.app"
LOAD_ENDPOINT = f"{RAILWAY_BASE}/tool/loadCorpus"
QUERY_ENDPOINT = f"{RAILWAY_BASE}/tool/queryCorpus"

# Read local PDF file already present in repo
pdf_path = "opengov2023.pdf"

# Extract PDF text
with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

# Call loadCorpus
payload = {
    "file_contents": text,
    "file_name": "Open Government Guidebook 2023",
    "metadata": {"source": "GoC", "year": 2023}
}
load_response = requests.post(LOAD_ENDPOINT, json=payload)
print("\n📥 loadCorpus response:")
print(load_response.json())

# Run test queries
queries = [
    "open government policy objectives",
    "transparency and digital services"
]

for q in queries:
    query_response = requests.post(QUERY_ENDPOINT, json={"query": q})
    print(f"\n🔍 Query: {q}")
    print(query_response.json().get("answer"))