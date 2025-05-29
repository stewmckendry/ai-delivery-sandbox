from datetime import datetime
from app.db.models.ProjectProfile import ProjectProfile
from app.db.database import get_session
import yaml
from jinja2 import Template
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
import json
import logging
logger = logging.getLogger(__name__)

class ProjectProfileEngine:
    def load_profile(self, project_id: str) -> dict:
        db = get_session()
        profile = db.query(ProjectProfile).filter(ProjectProfile.project_id == project_id).first()
        logger.info(f"Loaded project profile for ID: {project_id}")
        return profile.to_dict() if profile else {}

    def save_profile(self, profile_dict: dict) -> dict:
        db = get_session()
        profile = db.query(ProjectProfile).filter(ProjectProfile.project_id == profile_dict["project_id"]).first()
        if profile:
            for key, value in profile_dict.items():
                setattr(profile, key, value)
        else:
            profile = ProjectProfile(**profile_dict)
            db.add(profile)
        db.commit()
        logger.info(f"Saved project profile for ID: {profile_dict['project_id']}")
        return profile.to_dict()

    def generate_and_save(self, text, metadata, existing=None):
        try:
            prior = "\n".join([f"{k}: {v}" for k, v in existing.items()]) if existing else ""
            prompt_vars = {
                "project_id": metadata.get("project_id", ""),
                "input_text": text,
                "prior": prior
            }

            template = get_prompt("project_profile_prompts.yaml", "generate_project_profile")
            system_prompt = template.get("system", "")
            user_template = template.get("user", "")
            user_prompt = user_template.format(**prompt_vars)

            output = chat_completion_request(system_prompt, user_prompt)

            logger.info(f"LLM output: {output}")

            if isinstance(output, str):
                output = json.loads(output)

            profile_data = output.get("project_profile", {})
            profile_data["project_id"] = metadata.get("project_id")
            logger.info(f"Generated project profile: {profile_data}")
            return self.save_profile(profile_data)

        except Exception as e:
            logger.error(f"Failed to generate project profile: {e}")
            return None
