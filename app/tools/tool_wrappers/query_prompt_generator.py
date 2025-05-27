import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "project_profile" not in input_dict:
            raise ValueError("Missing required field: project_profile")
        if "memory" not in input_dict:
            raise ValueError("Missing required field: memory")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        profile = input_dict.get("project_profile", {})
        memory = input_dict.get("memory", [])

        profile_summary = "\n".join([
            f"Project Title: {profile.get('title', 'N/A')}",
            f"Scope Summary: {profile.get('scope_summary', '')}",
            f"Strategic Alignment: {profile.get('strategic_alignment', '')}",
            f"Stakeholders: {profile.get('key_stakeholders', '')}",
            f"Project Type: {profile.get('project_type', '')}"
        ])

        memory_lines = []
        for entry in memory:
            if isinstance(entry, dict):
                if "input_summary" in entry:
                    memory_lines.append(entry["input_summary"])
                elif "text" in entry:
                    memory_lines.append(entry["text"][:200])

        memory_context = "\n".join(memory_lines[:10])

        prompt = f"""
You are an assistant helping a policy analyst formulate a concise, rich search query.
Use the following project context and memory to generate a query for searching government documentation.

[Project Context]
{profile_summary}

[Memory Extracts]
{memory_context}

Provide a single query that captures the key themes and information needs.
"""

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You generate search queries for analysts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        return {"query": response.choices[0].message.content.strip()}