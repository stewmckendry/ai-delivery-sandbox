from app.db.database import get_session
from app.db.models.ProjectProfile import ProjectProfile
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ProjectProfileEngine:
    def save_profile(self, profile_data: dict):
        session = get_session()
        logger.debug(f"Saving project profile: {profile_data}")
        for k, v in profile_data.items():
            logger.debug(f"DB save field {k}: {v} ({type(v)})")
        profile = session.query(ProjectProfile).get(profile_data['project_id'])
        if not profile:
            profile = ProjectProfile(**profile_data)
            session.add(profile)
        else:
            for key, value in profile_data.items():
                logger.debug(f"Updating {key} to {value} ({type(value)})")
                setattr(profile, key, value)
            profile.last_updated = datetime.utcnow()
        session.commit()
        logger.info(f"Project profile saved for ID: {profile.project_id}")
        return profile.project_id

    def load_profile(self, project_id: str) -> dict:
        session = get_session()
        profile = session.query(ProjectProfile).get(project_id)
        if not profile:
            logger.warning(f"No profile found for project_id: {project_id}")
            raise NoResultFound(f"No profile found for project_id: {project_id}")
        profile_dict = {c.name: getattr(profile, c.name) for c in profile.__table__.columns}
        logger.debug(f"Loaded project profile: {profile_dict}")
        return profile_dict

    def validate_profile(self, profile_data: dict) -> bool:
        required_fields = ["project_id", "title"]
        for field in required_fields:
            if field not in profile_data:
                logger.error(f"Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")
        return True