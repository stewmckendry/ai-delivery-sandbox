import os
import yaml
import uuid
import datetime
from app.tools.tool_wrappers.structured_input_ingestor import structure_input
from app.engines.memory_sync import log_tool_usage
from app.utils.trace_utils import write_trace
from app.engines.project_profile_engine import ProjectProfileEngine

class Tool:
    def validate(self, input_dict):
        # placeholder for validation logic
        pass

    def run_tool(self, input_dict, log_usage=True):
        self.validate(input_dict)
        text = input_dict["text"]
        metadata = input_dict.get("metadata") or {}
        project_id = metadata.get("project_id")

        entry = structure_input(text, source="direct_input", tool_name="uploadTextInput", metadata=metadata)
        out_path = write_trace(entry)
        if log_usage:
            log_tool_usage(
                entry["tool"],
                entry["input_summary"],
                entry["output_summary"],
                session_id=entry.get("session_id"),
                user_id=entry.get("user_id"),
                metadata=entry.get("metadata")
            )

        if input_dict.get("save_profile", False):
            ProjectProfileEngine().generate_and_save(text, metadata)

        return {
            "status": "success",
            "path": out_path,
            "text": text,
            "metadata": metadata,
            "project_id": project_id
        }