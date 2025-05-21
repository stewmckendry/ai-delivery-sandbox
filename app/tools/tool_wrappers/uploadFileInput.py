import os
import yaml
import uuid
import datetime
from app.tools.tool_wrappers.text_extractor import extract_text
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.tools.tool_wrappers.retry_ingestion import retry_with_backoff

def uploadFileInput(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")

    raw = retry_with_backoff(extract_text, file_path=file_path)
    if raw is None:
        raise ValueError("Failed to extract text from file.")

    entry = structure_input(raw, file_path, "uploadFileInput")
    trace_path = os.path.join("logs", "ingest_traces")
    os.makedirs(trace_path, exist_ok=True)
    out_path = os.path.join(trace_path, f"{entry['id']}.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump([entry], f, sort_keys=False)

    return {"status": "success", "path": out_path}