import os
import re
from string import Template
from dotenv import load_dotenv
from app.schemas.section_draft_output import SectionDraftOutput
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template
import logging
logger = logging.getLogger(__name__)
import requests
import yaml

load_dotenv()

class Tool:
    def get_section_intents(self, gate_id, artifact_id, section_id):
        url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"
        try:
            response = requests.get(url)
            response.raise_for_status()
            gate_data = yaml.safe_load(response.text)

            for gate in gate_data:
                if str(gate.get("gate_id")) == str(gate_id):
                    for artifact in gate.get("artifacts", []):
                        if artifact.get("artifact_id") == artifact_id:
                            for section in artifact.get("sections", []):
                                if section.get("section_id") == section_id:
                                    return section.get("intents", [])
            return []
        except Exception as e:
            print(f"Error fetching section intents: {e}")
            return []
        
    def run_tool(self, input_dict):
        logger.info("[Tool] section_synthesizer started")
        memory_summary = input_dict.get("memory_summary", [])
        global_context_summary = input_dict.get("global_context_summary", [])
        context_summary = input_dict.get("context_summary", "")
        prior_artifacts_summary = input_dict.get("prior_artifacts_summary", "")

        artifact = input_dict.get("artifact_id")
        section = input_dict.get("section_id")
        gate = input_dict.get("gate_id", "0")

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

        section_intents = self.get_section_intents(gate, artifact, section)

        prompt_templates = get_prompt("generate_section_prompts.yaml", "section_synthesis")
        user_template = Template(prompt_templates["user"])
        user_prompt = user_template.render(
            artifact=artifact,
            section=section,
            profile_context=profile_context,
            context_summary=context_summary,
            memory_str=memory_summary,
            global_context_str=global_context_summary,
            section_intents=section_intents,
            prior_artifacts_summary=prior_artifacts_summary
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