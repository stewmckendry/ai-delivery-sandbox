from datetime import datetime
from app.db.models.ProjectProfile import ProjectProfile
from app.db.database import db
from app.tools.utils.llm_helpers import run_llm_prompt
import yaml
from jinja2 import Template

class ProjectProfileEngine:
    def load_profile(self, project_id: str) -> dict:
        profile = db.query(ProjectProfile).filter(ProjectProfile.project_id == project_id).first()
        return profile.to_dict() if profile else {}

    def save_profile(self, profile_dict: dict) -> dict:
        profile = db.query(ProjectProfile).filter(ProjectProfile.project_id == profile_dict["project_id"]).first()
        if profile:
            for key, value in profile_dict.items():
                setattr(profile, key, value)
        else:
            profile = ProjectProfile(**profile_dict)
            db.add(profile)
        db.commit()
        return profile.to_dict()

    def generate_and_save(self, text: str, metadata: dict, existing: dict = None) -> dict:
        project_id = metadata.get("project_id")
        if not project_id:
            raise ValueError("Missing project_id")

        existing = existing or {}
        prior = "".join([f"{k}: {v}\n" for k, v in existing.items()]) if existing else ""

        with open("app/prompts/project_profile_prompts.yaml") as f:
            prompt_config = yaml.safe_load(f)

        system_msg = prompt_config["prompts"]["generate_project_profile"]["system"]
        user_template = Template(prompt_config["prompts"]["generate_project_profile"]["user"])
        user_msg = user_template.render(project_id=project_id, input_text=text, prior=prior)

        response = run_llm_prompt(system_msg, user_msg)
        output = response.get("project_profile", response)

        output["project_id"] = output.get("project_id") or project_id
        output["last_updated"] = datetime.utcnow()

        return self.save_profile(output)