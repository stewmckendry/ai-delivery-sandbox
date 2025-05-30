import logging
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from app.engines.memory_sync import log_tool_usage
from jinja2 import Template

logger = logging.getLogger(__name__)


class Tool:

    def run_tool(self, input_dict):
        
        logger.info("[Tool] record_research started")

        notes = input_dict["notes"]
        session_id = input_dict.get("session_id")
        project_id = input_dict.get("project_id")
        user_id = input_dict.get("user_id", "unknown")

        prompt_templates = get_prompt("search_prompts.yaml", "search_cleanup")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(raw_input=notes)

        logger.info(f"[record_research] Cleaning up notes with prompt: {user_prompt[:100]}...")
        result = chat_completion_request(system_prompt, user_prompt, temperature=0.3)

        # Wrap into structured response
        output_summary = {
            "answer": result,
            "documents": [notes],
            "citations": [f"User-supplied notes. {user_id}, session {session_id}."],
            "metadatas": [{
                "text": notes,
                "title": "User Notes",
                "source": "User",
                "date": "n.d.",
                "url": "",
                "citation": f"User-supplied notes. {user_id}, session {session_id}."
            }]
        }

        log_tool_usage("record_research", "global_context | record_research", output_summary, session_id, user_id, input_dict)
        return output_summary
