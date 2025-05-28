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
        upload_tool = self.registry.get_tool(tool_map[method])
        upload_result = upload_tool.run_tool(inputs, log_usage=False)

        raw_text = upload_result.get("text")
        metadata = upload_result.get("metadata", {})
        logger.debug(f"Raw text extracted: {raw_text[:100]}")
        logger.debug(f"Metadata: {metadata}")

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

        logger.debug(f"Generated project profile: {project_profile}")
        for k, v in project_profile.items():
            logger.debug(f"Generated field {k}: {v} ({type(v)})")

        if not project_profile.get("project_id"):
            logger.info("LLM output missing project_id, using metadata project_id")
            project_profile["project_id"] = metadata_project_id

        project_profile["last_updated"] = datetime.utcnow()
        logger.debug("Added last_updated field")

        def clean(field, expected_type):
            val = project_profile.get(field)
            if val == "":
                val = None
            if val is None:
                project_profile[field] = None
                return
            try:
                if expected_type == "date":
                    project_profile[field] = datetime.strptime(val, "%Y-%m-%d").date()
                elif expected_type == "int":
                    project_profile[field] = int(val)
                elif expected_type == "float":
                    project_profile[field] = float(val)
            except Exception as e:
                logger.warning(f"Invalid {expected_type} format for {field}: {val}, setting to None")
                project_profile[field] = None

        for field in ["start_date", "end_date"]:
            clean(field, "date")
        clean("total_budget", "float")
        clean("current_gate", "int")

        project_id = project_profile.get("project_id")
        if not project_id:
            logger.error("Final project_profile missing project_id")
            raise ValueError("Missing project_id in generated profile")

        try:
            old = ProjectProfileEngine().load_profile(project_id)
            for k, v in project_profile.items():
                if v is not None or old.get(k) in ("", None):
                    old[k] = v
            project_profile = old
            logger.info(f"Merged with existing profile for ID: {project_id}")
        except:
            logger.info(f"No merge needed for new project_id: {project_id}")

        logger.info(f"Saving cleaned project profile: {json.dumps(project_profile, indent=2, default=str)}")
        for key, value in project_profile.items():
            logger.debug(f"Before DB save: {key} type: {type(value)} value: {value}")

        ProjectProfileEngine().save_profile(project_profile)
        logger.info(f"Saved project profile for ID: {project_id}")

        log_tool_usage(
            tool_name=tool_map[method],
            input_summary=f"{inputs.get(method) or inputs.get('file_path')} | {tool_map[method]}",
            output_summary=raw_text[:200],
            session_id=metadata.get("session_id"),
            user_id=metadata.get("user_id"),
            metadata=metadata
        )

        return {
            "status": "profile_saved",
            "project_id": project_id,
            "project_profile": project_profile,
            "text": raw_text,
            "metadata": metadata
        }

