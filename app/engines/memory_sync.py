import json
import os
from datetime import datetime

MEMORY_LOG_PATH = "logs/prompt_logs.jsonl"
SESSION_SNAPSHOT_PATH = "logs/session_snapshots/"

os.makedirs(os.path.dirname(MEMORY_LOG_PATH), exist_ok=True)
os.makedirs(SESSION_SNAPSHOT_PATH, exist_ok=True)

def log_tool_usage(tool_name, input_data, output_data):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "tool": tool_name,
        "input": input_data,
        "output": output_data
    }
    with open(MEMORY_LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def save_session_snapshot(state):
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    path = os.path.join(SESSION_SNAPSHOT_PATH, f"snapshot_{timestamp}.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def load_latest_snapshot():
    files = sorted(os.listdir(SESSION_SNAPSHOT_PATH), reverse=True)
    if not files:
        return {}
    with open(os.path.join(SESSION_SNAPSHOT_PATH, files[0]), "r") as f:
        return json.load(f)