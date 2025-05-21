# app/utils/trace_utils.py
import os
import yaml

def is_cloud_env():
    return os.getenv("RAILWAY_ENVIRONMENT") is not None

def write_trace(entry, trace_dir="logs/ingest_traces"):
    if is_cloud_env():
        print("Skipping trace write: running in cloud environment")
        return None

    os.makedirs(trace_dir, exist_ok=True)
    out_path = os.path.join(trace_dir, f"{entry['id']}.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump([entry], f, sort_keys=False)
    return out_path
