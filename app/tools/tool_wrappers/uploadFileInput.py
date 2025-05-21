import os
import yaml
import uuid
import datetime
from app.tools.tool_wrappers.text_extractor import extract_text
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.tools.tool_wrappers.retry_ingestion import retry_with_backoff
from app.engines.memory_sync import log_tool_usage
from app.utils.trace_utils import write_trace

class Tool:
    def validate(self, input_dict):
        if "file_path" not in input_dict and "file_contents" not in input_dict:
            raise ValueError("Must provide either 'file_path' or 'file_contents'.")

    def run_tool(self, input_dict):
        self.validate(input_dict)

        if "file_path" in input_dict:
            file_path = input_dict["file_path"]
            raw = retry_with_backoff(extract_text, file_path=file_path)
            source = file_path
        else:
            raw = input_dict["file_contents"]
            source = "uploaded_file"

        if raw is None:
            raise ValueError("Failed to extract or read text from file.")

        entry = structure_input(raw, source, tool_name="uploadFileInput")
        out_path = write_trace(entry)

        log_tool_usage(
            entry["tool"],
            entry["input_summary"],
            entry["output_summary"],
            full_input_path=out_path if "file_path" in input_dict else None,
            full_output_path=entry.get("full_output_path"),
            session_id=entry.get("session_id"),
            user_id=entry.get("user_id")
        )

        return {"status": "success", "path": out_path}