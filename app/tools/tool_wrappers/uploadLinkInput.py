import os
import yaml
import uuid
import datetime
import requests
from bs4 import BeautifulSoup
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.engines.memory_sync import log_tool_usage

class Tool:
    def validate(self, input_dict):
        # placeholder for validation logic
        pass

    def run_tool(self, input_dict):
        self.validate(input_dict)
        url = input_dict["url"]
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
        except Exception as e:
            raise ValueError(f"Error fetching or parsing URL: {e}")

        entry = structure_input(text, url, tool_name="uploadLinkInput")
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