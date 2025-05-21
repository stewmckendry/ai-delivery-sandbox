import os
import yaml
import datetime
import uuid

def uploadTextInput(text: str, source: str = "user"):
    entry = {
        'id': str(uuid.uuid4()),
        'source': source,
        'type': 'uploadTextInput',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'content_summary': text[:1000],
        'tags': ['input', 'text']
    }
    trace_path = os.path.join("logs", "ingest_traces")
    os.makedirs(trace_path, exist_ok=True)
    out_path = os.path.join(trace_path, f"{entry['id']}.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump([entry], f, sort_keys=False)
    return {"status": "success", "path": out_path}