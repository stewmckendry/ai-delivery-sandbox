from pydantic import BaseModel, parse_obj_as
from typing import Optional
from app.engines.project_profile_engine import ProjectProfileEngine
import logging

logger = logging.getLogger(__name__)

class InputSchema(BaseModel):
    project_id: str

class OutputSchema(BaseModel):
    project_profile: dict
    editable: bool = True

class Tool:
    def run_tool(self, input_dict):
        input_data = parse_obj_as(InputSchema, input_dict)
        logger.info(f"Loading project profile for project_id: {input_data.project_id}")

        profile = ProjectProfileEngine().load_profile(input_data.project_id)
        logger.info(f"Loaded profile: {profile}")

        return OutputSchema(project_profile=profile).dict()