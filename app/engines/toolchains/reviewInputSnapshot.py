import logging
from app.db.models.PromptLog import PromptLog
from app.db.database import get_session
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template

logger = logging.getLogger(__name__)

class Tool:

    def run_tool(self, input_dict):
        logger.info("[Tool] reviewInputSnapshot started")

        project_id = input_dict["project_id"]
        session_id = input_dict["session_id"]

        tool_names = ["record_research", "queryCorpus", "uploadTextInput", "uploadFileInput", "uploadLinkInput"]

        session = get_session()
        query = session.query(PromptLog).filter(
            PromptLog.tool.in_(tool_names),
            PromptLog.project_id == project_id,
            PromptLog.session_id == session_id
        )
        entries = query.order_by(PromptLog.timestamp.asc()).all()

        summaries = [f"Tool: {e.tool}\nInput: {e.input_summary}\nOutput: {e.output_summary}" for e in entries]
        input_text = "\n\n".join(summaries)

        prompt_templates = get_prompt("revision_prompts.yaml", "input_snapshot")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(inputs=input_text)

        logger.info("[Tool] Calling LLM with input snapshot prompt")
        result = chat_completion_request(system_prompt, user_prompt, temperature=0.4)

        return {
            "input_snapshot": result,
            "instructions": "This snapshot summarizes all inputs uploaded during this session. Use it to inform drafting and revisions."
        }