import logging
import uuid
import os
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage
from jinja2 import Template
from app.engines.project_profile_engine import ProjectProfileEngine
from app.engines.toolchains.global_context_chain import GlobalContextChain
from app.db.models.ArtifactSection import ArtifactSection
from app.db.database import SessionLocal
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
import requests
import yaml
from app.redis.redis_client import redis_client
import json

logger = logging.getLogger(__name__)

class GenerateSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")
        self.global_context_engine = GlobalContextChain()
    
    def summarize_drafted_sections(self, artifact_id, session_id, project_id):
        db = SessionLocal()
        sections = db.query(ArtifactSection).filter_by(artifact_id=artifact_id, project_id=project_id, session_id=session_id).all()
        # Remove duplicates based on section text
        unique_texts = set()
        unique_sections = []
        for s in sections:
            if s.text not in unique_texts:
                unique_texts.add(s.text)
                unique_sections.append(s)
        sections = unique_sections

        if not sections:
            return ""

        text_blob = "\n\n".join([f"{s.section_id}: {s.text}" for s in sections])
        prompt_templates = get_prompt("generate_section_prompts.yaml", "drafted_sections_synthesis")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(text_blob=text_blob)

        return chat_completion_request(system_prompt, user_prompt)


    def summarize_memory(self, memory_entries):
        content_blocks = [entry.get("output_summary", "") for entry in memory_entries if entry.get("output_summary")]
        if not content_blocks:
            return ""

        combined_text = "\n\n".join(content_blocks)
        prompt_templates = get_prompt("generate_section_prompts.yaml", "memory_summary_synthesis")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(content=combined_text)

        return chat_completion_request(system_prompt, user_prompt, temperature=0.3)


    def run(self, inputs, global_context=None):
        trace = []
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact_id")
        section_id = inputs.get("section_id")
        gate_id = inputs.get("gate_id", "0")
        project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

        #load project profile if available
        if project_id:
            profile_engine = ProjectProfileEngine()
            project_profile = profile_engine.load_profile(project_id)
        else:
            project_profile = {}
        inputs["project_profile"] = project_profile

        context_summary = self.summarize_drafted_sections(artifact_id, session_id, project_id)
        log_tool_usage("context_summary", "summarized prior sections", context_summary, session_id, user_id, inputs)

        memory_input = {**inputs}
        memory_input["project_profile"] = project_profile

        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        memory_summary = self.summarize_memory(memory)
        log_tool_usage("memory_summary", "summarized memory context", memory_summary, session_id, user_id, inputs)
        logger.info("[Step 2] memory_summary complete")

        if global_context is None:
            context_data = self.global_context_engine.fetch_logged_global_context(project_id, session_id)
            global_context = {
                "summary": self.global_context_engine.summarize_global_context(context_data),
                **context_data
            }
            log_tool_usage("global_context", "fetched global context", context_data, session_id, user_id, inputs)
            log_tool_usage("global_context", "summarized global context", global_context["summary"], session_id, user_id, inputs)
            logger.info("[Step 3] global_context complete")

        structured_inputs = {
            "memory_summary": memory_summary,
            "global_context_summary": global_context["summary"],
            "context_summary": context_summary
        }

        draft = self.synth_tool.run_tool({**inputs, **structured_inputs})
        log_tool_usage("section_synthesizer", "generated draft", draft, session_id, user_id, inputs)
        trace.append({"tool": "section_synthesizer", "output": draft})
        logger.info("[Step 4] section_synthesizer complete")

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        log_tool_usage("section_refiner", "refined draft", refined, session_id, user_id, inputs)
        trace.append({"tool": "section_refiner", "output": refined})
        logger.info("[Step 5] section_refiner complete")

        # Cache in Redis for iteration workflows
        try:
            key = f"section_revision:{project_id}:{artifact_id}:{section_id}"
            redis_payload = {
                "text": refined["raw_draft"],
                "diff_summary": None,  # none yet
                "status": "completed"
            }
            redis_client.set(key, json.dumps(redis_payload))
            logger.info(f"[Redis] Cached section to key {key}")
        except Exception as e:
            logger.error(f"[Redis] Failed to cache section revision: {e}")

        save_result = save_artifact_and_trace(
            section_id=section_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            text=refined["raw_draft"],
            sources=draft.get("prompt_used"),
            tool_outputs=trace,
            user_id=user_id,
            project_id=project_id,
            session_id=session_id
        )
        logger.info("[Step 6] Saved to ArtifactSection and ReasoningTrace")

        return {"final_output": refined, "trace": trace, "save_result": save_result}