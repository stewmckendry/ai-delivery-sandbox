import os
import logging
import json
from openai import OpenAI
from datetime import datetime
from app.engines.project_profile_engine import ProjectProfileEngine
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage

logger = logging.getLogger(__name__)

class IngestInputChain:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.registry = ToolRegistry()

    def run(self, inputs: dict):
        method = inputs.get("input_method")
        logger.info(f"Running IngestInputChain with method: {method}")
        if method not in ["text", "file", "link"]:
            raise ValueError("input_method must be one of: text, file, link")

        tool_map = {
            "text": "uploadTextInput",
            "file": "uploadFileInput",
            "link": "uploadLinkInput"
        }
        logger.info(f"Running tool: {tool_map[method]} for method: {method}")
        upload_tool = self.registry.get_tool(tool_map[method])
        upload_result = upload_tool.run_tool(inputs, log_usage=False)

        raw_text = upload_result.get("text")
        metadata = upload_result.get("metadata", {})
        metadata_project_id = inputs.get("project_id")
        if not metadata_project_id:
            logger.error("Input metadata missing required project_id")
            raise ValueError("Input metadata must include project_id")

        try:
            existing = ProjectProfileEngine().load_profile(metadata_project_id)
            logger.info(f"Loaded existing project profile for ID: {metadata_project_id}")
        except Exception as e:
            logger.warning(f"No existing profile found or load failed: {e}")
            existing = {}

        project_profile = ProjectProfileEngine().generate_and_save(text=raw_text, metadata=metadata, existing=existing)
        project_id = project_profile.get("project_id", metadata_project_id)
        logger.info(f"Generated and saved project profile: {project_id}")

        log_tool_usage(
            tool_name=tool_map[method],
            input_summary=f"{inputs.get(method) or inputs.get('file_path')} | {tool_map[method]}",
            output_summary=raw_text[:200],
            session_id=metadata.get("session_id"),
            user_id=metadata.get("user_id"),
            metadata=metadata
        )
        logger.info("IngestInputChain completed successfully")
        return {
            "status": "profile_saved",
            "project_id": project_id,
            "project_profile": project_profile,
            "text": raw_text,
            "metadata": metadata
        }

