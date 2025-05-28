class ProjectProfileEngine:
    def save_profile(self, profile):
        from app.db.models.ProjectProfile import ProjectProfile
        from app.db.database import SessionLocal
        from sqlalchemy.orm import Session

        with SessionLocal() as session:
            existing = session.query(ProjectProfile).filter_by(project_id=profile["project_id"]).first()
            if existing:
                for k, v in profile.items():
                    setattr(existing, k, v)
            else:
                session.add(ProjectProfile(**profile))
            session.commit()

    def load_profile(self, project_id):
        from app.db.models.ProjectProfile import ProjectProfile
        from app.db.database import SessionLocal
        with SessionLocal() as session:
            profile = session.query(ProjectProfile).filter_by(project_id=project_id).first()
            return profile.to_dict() if profile else {}

    def generate_profile_from_text(self, text: str, metadata: dict, existing: dict = None) -> dict:
        from app.tools.utils.llm_helpers import chat_completion_request
        import json
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
You are a project analyst. Your task is to build a structured project profile.
The project ID is: {metadata.get('project_id')}

Extract fields only if they are supported by the text. Use null where missing.

{schema}
{prior_text}

INPUT TEXT:
{text}

---
"""
        return json.loads(chat_completion_request("system", prompt))