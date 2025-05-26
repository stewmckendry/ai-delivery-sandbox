import os
import logging
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

        metadata_project_id = metadata.get("project_id")
        if not metadata_project_id:
            logger.error("Input metadata missing required project_id")
            raise ValueError("Input metadata must include project_id")

        try:
            existing = ProjectProfileEngine().load_profile(metadata_project_id)
            logger.info(f"Loaded existing project profile for ID: {metadata_project_id}")
        except Exception as e:
            logger.warning(f"No existing profile found or load failed: {e}")
            existing = {}

        project_profile = self.generate_project_profile(raw_text, metadata, existing)
        logger.debug(f"Generated project profile: {project_profile}")

        if not project_profile.get("project_id"):
            logger.info("LLM output missing project_id, using metadata project_id")
            project_profile["project_id"] = metadata_project_id

        project_profile["last_updated"] = datetime.utcnow().isoformat()

        def clean(field, expected_type):
            val = project_profile.get(field)
            if val == "" or val is None:
                project_profile[field] = None
            elif expected_type == "date":
                try:
                    datetime.strptime(val, "%Y-%m-%d")
                except:
                    logger.warning(f"Invalid date format for {field}: {val}, setting to None")
                    project_profile[field] = None

        for field in ["start_date", "end_date"]:
            clean(field, "date")
        for field in ["total_budget"]:
            if project_profile.get(field) == "":
                project_profile[field] = None
        for field in ["current_gate"]:
            if isinstance(project_profile.get(field), str) and not project_profile[field].isdigit():
                project_profile[field] = None

        project_id = project_profile.get("project_id")
        if not project_id:
            logger.error("Final project_profile missing project_id")
            raise ValueError("Missing project_id in generated profile")

        try:
            old = ProjectProfileEngine().load_profile(project_id)
            old.update({k: v for k, v in project_profile.items() if v})
            project_profile = old
            logger.info(f"Merged with existing profile for ID: {project_id}")
        except:
            logger.info(f"No merge needed for new project_id: {project_id}")

        ProjectProfileEngine().save_profile(project_profile)
        logger.info(f"Saved project profile for ID: {project_id}")

        log_tool_usage(
            tool=tool_map[method],
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

    def generate_project_profile(self, text: str, metadata: dict, existing: dict = None) -> dict:
        schema = """
project_profile:
  project_id: string
  title: string
  sponsor: string
  project_type: string
  total_budget: number (use null if missing)
  start_date: date (YYYY-MM-DD, use null if missing)
  end_date: date (YYYY-MM-DD, use null if missing)
  strategic_alignment: string
  current_gate: integer (use null if missing)
  scope_summary: string
  key_stakeholders: string
  major_risks: string
  resource_summary: string
  last_updated: datetime (use null if missing)
        """

        prior = "".join([f"{k}: {v}\n" for k, v in existing.items()]) if existing else ""
        prior_text = f"\nExisting profile:\n{prior}" if prior else ""

        prompt = f"""
You are a project analyst. From the following text, extract a structured project profile in this format:
{schema}

Only include data present in the input. Leave missing fields blank or use null.
{prior_text}

INPUT TEXT:
{text}
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Extract a JSON object that fits the project_profile schema."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        raw_output = response.choices[0].message.content.strip()
        logger.debug(f"Raw LLM output: {raw_output}")
        try:
            parsed = eval(raw_output)
            if "project_profile" in parsed:
                parsed = parsed["project_profile"]
                logger.debug("Unwrapped nested 'project_profile' key from LLM output")
            return parsed
        except Exception as e:
            logger.error(f"Failed to parse output: {e}\nRaw output: {raw_output}")
            raise ValueError(f"Failed to parse output: {e}\nRaw output: {raw_output}")