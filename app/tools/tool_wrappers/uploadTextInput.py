import os
import yaml
import uuid
import datetime
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.engines.memory_sync import log_tool_usage

class Tool:
    def validate(self, input_dict):
        if "text" not in input_dict:
            raise ValueError("Missing 'text' in input.")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        text = input_dict["text"]
        entry = structure_input(text, source="direct_input", tool_name="uploadTextInput")

        trace_path = os.path.join("logs", "ingest_traces")
        os.makedirs(trace_path, exist_ok=True)
        out_path = os.path.join(trace_path, f"{entry['id']}.yaml")
        with open(out_path, "w", encoding="utf-8") as f:
            yaml.dump([entry], f, sort_keys=False)

        log_tool_usage(
            entry["tool"],
            entry["input_summary"],
            entry["output_summary"],
            full_input_path=out_path,
            full_output_path=entry.get("full_output_path"),
            session_id=entry.get("session_id"),
            user_id=entry.get("user_id")
        )

        return {"status": "success", "path": out_path}