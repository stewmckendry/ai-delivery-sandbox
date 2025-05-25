import os
from openai import OpenAI
from datetime import datetime
from app.engines.project_profile_engine import ProjectProfileEngine
from app.tools.tool_registry import ToolRegistry

class IngestInputChain:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.registry = ToolRegistry()

    def run(self, inputs: dict):
        method = inputs.get("input_method")
        if method not in ["text", "file", "link"]:
            raise ValueError("input_method must be one of: text, file, link")

        tool_map = {
            "text": "uploadTextInput",
            "file": "uploadFileInput",
            "link": "uploadLinkInput"
        }
        upload_tool = self.registry.get_tool(tool_map[method])
        upload_result = upload_tool.run_tool(inputs)

        raw_text = upload_result.get("text")
        metadata = upload_result.get("metadata", {})
        user_id = inputs.get("user_id")

        try:
            project_id = metadata.get("project_id")
            existing = ProjectProfileEngine().load_profile(project_id)
        except:
            existing = {}

        project_profile = self.generate_project_profile(raw_text, metadata, existing)
        project_profile["last_updated"] = datetime.utcnow().isoformat()

        project_id = project_profile.get("project_id")
        if not project_id:
            raise ValueError("Missing project_id in generated profile")

        try:
            old = ProjectProfileEngine().load_profile(project_id)
            old.update({k: v for k, v in project_profile.items() if v})
            project_profile = old
        except:
            pass

        ProjectProfileEngine().save_profile(project_profile)
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

        prior = "".join([f"{k}: {v}\n" for k, v in existing.items()]) if existing else ""
        prior_text = f"\nExisting profile:\n{prior}" if prior else ""

        prompt = f"""
You are a project analyst. From the following text, extract a structured project profile in this format:
{schema}

Only include data present in the input. Leave missing fields blank.
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
        try:
            return eval(raw_output)
        except Exception as e:
            raise ValueError(f"Failed to parse output: {e}\nRaw output: {raw_output}")