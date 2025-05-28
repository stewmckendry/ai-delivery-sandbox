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
        memory = input_dict.get("memory", [])
        alignment_results = input_dict.get("alignment_results", [])
        web_summary = input_dict.get("web_search", "")
        corpus_answer = input_dict.get("corpus_answer", {})
        context_summary = input_dict.get("context_summary", "")

        def format_sources(label, entries):
            lines = []
            for entry in entries:
                if isinstance(entry, dict):
                    if "input_summary" in entry and "full_input_path" in entry:
                        lines.append(f"- {entry['input_summary']}: {entry['full_input_path']}")
                    elif "title" in entry and "url" in entry:
                        lines.append(f"- {entry['title']}: {entry['url']}")
                    elif "content" in entry:
                        lines.append(f"- {entry['content'][:200]}...")
                    elif "text" in entry:
                        lines.append(f"- {entry['text'][:200]}...")
            return f"\n{label} Sources:\n" + "\n".join(lines) if lines else ""

        memory_str = format_sources("Project Documentation and Historical Inputs", memory)
        alignment_str = format_sources("Government of Canada Strategic Alignment", alignment_results)
        corpus_answer_str = "\nEmbedded Government Reports and Policies:\n" + corpus_answer.get("answer", "") if corpus_answer else ""
        web_str = f"\nExternal Web Insights:\n{web_summary}" if web_summary else ""

        artifact = input_dict.get("artifact")
        section = input_dict.get("section")

        profile = input_dict.get("project_profile", {})
        profile_context = ""
        if profile:
            profile_context = f"""
[Project Title]
{profile.get('title', 'N/A')}

[Scope Summary]
{profile.get('scope_summary', '')}

[Strategic Alignment]
{profile.get('strategic_alignment', '')}

[Stakeholders]
{profile.get('key_stakeholders', '')}

[Project Type]
{profile.get('project_type', '')}
            """

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