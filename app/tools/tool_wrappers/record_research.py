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

        if input_dict.get("metadatas"):
            metadatas = input_dict["metadatas"]
            citations = []
            for meta in metadatas:
                title = meta.get("title", "Untitled")
                source = meta.get("source", "Unknown")
                date = meta.get("date", "n.d.")
                url = meta.get("url", "")
                citation = f'"{title}." {source}, {date}, {url}.' if url else f'"{title}." {source}, {date}.'
                meta["citation"] = citation
                citations.append(citation)
        else:
            # Use GPT to structure the notes
            prompt_templates = get_prompt("search_prompts.yaml", "record_research_structuring")
            system_prompt = Template(prompt_templates["system"]).render()
            user_prompt = Template(prompt_templates["user"]).render(raw_input=notes)
            logger.info(f"[record_research] Structuring notes with prompt: {user_prompt[:100]}...")
            result = chat_completion_request(system_prompt, user_prompt, temperature=0.3)
            metadatas = result.get("structured", []) if isinstance(result, dict) else [{
                "text": notes,
                "title": "User Notes",
                "source": "User",
                "date": "n.d.",
                "url": ""
            }]
            for meta in metadatas:
                title = meta.get("title", "Untitled")
                source = meta.get("source", "Unknown")
                date = meta.get("date", "n.d.")
                url = meta.get("url", "")
                meta["citation"] = f'"{title}." {source}, {date}, {url}.' if url else f'"{title}." {source}, {date}.'
            citations = [m["citation"] for m in metadatas]

        output_summary = {
            "answer": notes,
            "documents": [m["text"] for m in metadatas],
            "citations": citations,
            "metadatas": metadatas
        }

        log_tool_usage("record_research", "global_context | record_research", output_summary, session_id, user_id, input_dict)
        logger.info(f"[Tool] record_research output summary: {output_summary['answer'][:100]}...")
        return output_summary
