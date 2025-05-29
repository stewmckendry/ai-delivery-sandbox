import logging
import requests
import yaml
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template

logger = logging.getLogger(__name__)

class Tool:

    def run_tool(self, input_dict):
        logger.info("[Tool] query_prompt_generator started")
        profile = input_dict.get("project_profile", {})
        memory = input_dict.get("memory", [])
        logger.info(f"[Tool] query_prompt_generator received profile: {profile}")
        logger.info(f"[Tool] query_prompt_generator received memory entries: {len(memory)}")
        
        summary_lines = []
        if profile.get('title'):
            summary_lines.append(f"Project Title: {profile['title']}")
        if profile.get('scope_summary'):
            summary_lines.append(f"Scope Summary: {profile['scope_summary']}")
        if profile.get('strategic_alignment'):
            summary_lines.append(f"Strategic Alignment: {profile['strategic_alignment']}")
        if profile.get('key_stakeholders'):
            summary_lines.append(f"Stakeholders: {profile['key_stakeholders']}")
        if profile.get('project_type'):
            summary_lines.append(f"Project Type: {profile['project_type']}")
        if summary_lines:
            profile_summary = "\n".join(summary_lines)
        else:
            profile_summary = "Project profile is not available."

        memory_lines = []
        for entry in memory:
            memory_lines.append(entry["output_summary"])

        memory_context = "\n".join(memory_lines)

        logger.info(f"Profile Summary: {profile_summary[:100]}...")  # Log first 100 characters for brevity
        logger.info(f"Memory Context: {memory_context[:100]}...")  # Log first 100 characters for brevity

        prompt_templates = get_prompt("generate_section_prompts.yaml", "search_query_generation")
        user_template = Template(prompt_templates["user"])
        user_prompt = user_template.render(
            profile_summary=profile_summary, memory_context=memory_context
        )
        system_prompt = prompt_templates["system"]        

        query = chat_completion_request(system=system_prompt, user=user_prompt).strip()
        logger.info(f"[Tool] prompt: {query.strip()[:100]}...")
        return {"query": query}
