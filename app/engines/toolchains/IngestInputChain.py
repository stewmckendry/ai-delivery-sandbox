import os
from openai import OpenAI
from datetime import datetime
from app.engines.project_profile_engine import ProjectProfileEngine

class IngestInputChain:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, inputs: dict):
        raw_text = inputs.get("text")
        metadata = inputs.get("metadata", {})
        user_id = inputs.get("user_id")

        project_profile = self.generate_project_profile(raw_text, metadata)
        project_profile["last_updated"] = datetime.utcnow().isoformat()

        project_id = project_profile.get("project_id")
        if not project_id:
            raise ValueError("Missing project_id in generated profile")

        try:
            existing = ProjectProfileEngine().load_profile(project_id)
            existing.update(project_profile)
            project_profile = existing
        except:
            pass

        ProjectProfileEngine().save_profile(project_profile)
        return {"status": "profile_saved", "project_id": project_id, "project_profile": project_profile}

    def generate_project_profile(self, text: str, metadata: dict) -> dict:
        schema = """
project_profile:
  project_id: string
  title: string
  sponsor: string
  project_type: string
  total_budget: number
  start_date: string
  end_date: string
  strategic_alignment: string
  current_gate: integer
  scope_summary: string
  key_stakeholders: string
  major_risks: string
  resource_summary: string
  last_updated: string
        """

        prompt = f"""
You are a project analyst. From the following text, extract a structured project profile in this format:
{schema}

Only include data present in the input. Leave missing fields blank.

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
        try:
            return eval(raw_output)
        except Exception as e:
            raise ValueError(f"Failed to parse output: {e}\nRaw output: {raw_output}")