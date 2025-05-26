import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from app.schemas.section_draft_output import SectionDraftOutput

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "memory" not in input_dict:
            raise ValueError("Missing required field: memory")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        memory = input_dict["memory"]

        context_lines = []
        for entry in memory:
            if "input_summary" in entry and "full_input_path" in entry:
                context_lines.append(f"- {entry['input_summary']}: {entry['full_input_path']}")
            elif "title" in entry and "url" in entry:
                context_lines.append(f"- {entry['title']}: {entry['url']}")

        context_str = "\n".join(context_lines)

        artifact = input_dict.get("artifact")
        section = input_dict.get("section")

        profile = input_dict.get("project_profile", {})
        profile_context = ""
        if profile:
            profile_context = f"""
Project Title: {profile.get('title', 'N/A')}
Scope Summary: {profile.get('scope_summary', '')}
Strategic Alignment: {profile.get('strategic_alignment', '')}
Stakeholders: {profile.get('key_stakeholders', '')}
Project Type: {profile.get('project_type', '')}
            """

        prompt = f"""
Based on the following user-provided inputs, draft a coherent and concise section draft. Keep it focused, factual, and well-structured.

Artifact: {artifact}
Section: {section}

Project Context:
{profile_context}

User Memory:
{context_str}

Begin the draft below:
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a policy analyst drafting high-quality documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw_draft = response.choices[0].message.content.strip()
        draft_chunks = re.split(r'\n\n+', raw_draft)

        return SectionDraftOutput(
            prompt_used=prompt,
            raw_draft=raw_draft,
            draft_chunks=draft_chunks
        ).dict()