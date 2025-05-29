import os
import re
from string import Template
from dotenv import load_dotenv
from app.schemas.section_draft_output import SectionDraftOutput
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template
import logging
logger = logging.getLogger(__name__)

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "memory" not in input_dict:
            raise ValueError("Missing required field: memory")

    def run_tool(self, input_dict):
        logger.info("[Tool] section_synthesizer started")
        self.validate(input_dict)
        memory_summary = input_dict.get("memory_summary", [])
        global_context_summary = input_dict.get("global_context_summary", [])
        context_summary = input_dict.get("context_summary", "")

        artifact = input_dict.get("artifact")
        section = input_dict.get("section")

        profile = input_dict.get("project_profile", {})
        profile_context = ""
        if profile:
            sections = []
            if profile.get('title'):
                sections.append(f"[Project Title]\n{profile['title']}")
            if profile.get('scope_summary'):
                sections.append(f"[Scope Summary]\n{profile['scope_summary']}")
            if profile.get('strategic_alignment'):
                sections.append(f"[Strategic Alignment]\n{profile['strategic_alignment']}")
            if profile.get('key_stakeholders'):
                sections.append(f"[Stakeholders]\n{profile['key_stakeholders']}")
            if profile.get('project_type'):
                sections.append(f"[Project Type]\n{profile['project_type']}")
            profile_context = "\n\n".join(sections) if sections else ""

        prompt_templates = get_prompt("generate_section_prompts.yaml", "section_synthesis")
        user_template = Template(prompt_templates["user"])
        user_prompt = user_template.render(
            artifact=artifact,
            section=section,
            profile_context=profile_context,
            context_summary=context_summary,
            memory_str=memory_str,
            corpus_answer_str=corpus_answer_str,
            alignment_str=alignment_str,
            web_str=web_str
        )

        system_prompt = prompt_templates["system"]
        logger.info(f"[Tool] section_synthesizer user prompt: {user_prompt[:250]}...")

        raw_draft = chat_completion_request(system_prompt, user_prompt, temperature=0.7)
        draft_chunks = re.split(r'\n\n+', raw_draft)
        logger.info(f"[Tool] section_synthesizer completed with raw draft: {raw_draft[:250]}...")
        return SectionDraftOutput(
            prompt_used=user_prompt,
            raw_draft=raw_draft,
            draft_chunks=draft_chunks
        ).dict()