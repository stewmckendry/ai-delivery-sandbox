import os
import yaml
import uuid
import datetime
import requests
from bs4 import BeautifulSoup
from app.tools.tool_wrappers.structured_input_ingestor import structure_input

schema = {
    "type": "object",
    "properties": {
        "url": {"type": "string", "format": "uri"}
    },
    "required": ["url"]
}

tool_name = "uploadLinkInput"

def run(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
    except Exception as e:
        raise ValueError(f"Error fetching or parsing URL: {e}")

    entry = structure_input(text, url, tool_name)
    trace_path = os.path.join("logs", "ingest_traces")
    os.makedirs(trace_path, exist_ok=True)
    out_path = os.path.join(trace_path, f"{entry['id']}.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump([entry], f, sort_keys=False)

    return {"status": "success", "path": out_path}