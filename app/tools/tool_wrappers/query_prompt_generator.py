import os
from dotenv import load_dotenv
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt

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

        prompts = get_prompt("generate_section_prompts.yaml", "search_query_generation")
        user_prompt_template = prompts["user"]
        user_prompt = user_prompt_template.render(profile_summary=profile_summary, memory_context=memory_context)
        system_prompt = prompts["system"]

        response = chat_completion_request(system_prompt, user_prompt)
        return {"query": response.strip()}
