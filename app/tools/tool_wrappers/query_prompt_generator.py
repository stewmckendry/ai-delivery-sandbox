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

        profile_summary = f"Title: {profile.get('title', '')}\nScope: {profile.get('scope_summary', '')}\nAlignment: {profile.get('strategic_alignment', '')}"

        memory_context = "\n".join([
            f"- {entry.get('input_summary', '')}: {entry.get('full_input_path', '')}" for entry in memory if entry.get('input_summary') and entry.get('full_input_path')
        ])

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
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return {"query": response.choices[0].message.content.strip(), "prompt_used": prompt}