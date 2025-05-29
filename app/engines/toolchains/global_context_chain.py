import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage
from app.engines.project_profile_engine import ProjectProfileEngine
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template
from app.db.models import PromptLog  # inline import to avoid circular dependency
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)

class GlobalContextChain:
    def __init__(self):
        registry = ToolRegistry()
        self.web_search_tool = registry.get_tool("webSearch")
        self.query_tool = registry.get_tool("query_prompt_generator")
        self.corpus_tool = registry.get_tool("queryCorpus")
        self.alignment_tool = registry.get_tool("goc_alignment_search")
        self.memory_tool = registry.get_tool("memory_retrieve")
    
    def summarize_web_results(self, search_results):
        if not search_results:
            return ""

        snippets = "\n".join([
            f"{entry['title']}: {entry['snippet']}"
            for entry in search_results if 'title' in entry and 'snippet' in entry
        ])
        prompt_templates = get_prompt("generate_section_prompts.yaml", "web_summary_synthesis")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(snippets=snippets)
        return chat_completion_request(system_prompt, user_prompt)


    def fetch_logged_global_context(self, project_id, session_id):
        db = SessionLocal()
        results = db.query(PromptLog).filter(
            and_(
                PromptLog.project_id == project_id,
                PromptLog.session_id == session_id,
                PromptLog.input_summary.like("global_context |%")
            )
        ).all()

        grouped_context = {"webSearch": [], "queryCorpus": [], "goc_alignment_search": []}
        for log in results:
            label = log.input_summary.split(" | ")[1]
            grouped_context.setdefault(label, []).append(log.output_summary)

        return grouped_context


    def summarize_global_context(self, grouped_context):
        from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
        from jinja2 import Template

        prompt_templates = get_prompt("generate_section_prompts.yaml", "global_context_synthesis")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(contexts=grouped_context)
        return chat_completion_request(system_prompt, user_prompt, temperature=0.3)


    def run(self, inputs):
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact_id")
        project_id = inputs.get("project_id")
        search_filter = inputs.get("search_filter", {}) # used in web_search for jurisdiction and market searches

        memory = self.memory_tool.run_tool({
            "artifact": artifact_id,
            "project_id": project_id,
            "session_id": session_id,
            "user_id": user_id
        })

        profile_engine = ProjectProfileEngine()
        project_profile = profile_engine.load_profile(project_id)

        # Step 1: Generate a smart search query
        query_payload = self.query_tool.run_tool({
            "project_profile": project_profile,
            "memory": memory
        })
        query_output = self.query_tool.run_tool(query_payload)
        search_query = query_output.get("query")
        log_tool_usage("queryPromptGenerator", "global_context | query_prompt_generator", query_output, session_id, user_id, inputs)

        # Step 2: Web Search
        web_results = self.web_search_tool.run_tool({
            "query": search_query,
            "search_type": "general",
            "context": search_filter
        })
        web_summary = self.summarize_web_results(web_results)
        log_tool_usage("webSearch", "global_context | webSearch", web_results, session_id, user_id, inputs)

        # Step 3: Embedded Corpus Search
        corpus_output = self.corpus_tool.run_tool({"query": search_query})
        log_tool_usage("queryCorpus", "global_context | queryCorpus", corpus_output, session_id, user_id, inputs)

        # Step 4: GoC Alignment
        alignment_output = self.alignment_tool.run_tool({"query": search_query})
        log_tool_usage("goc_alignment_search", "global_context | goc_alignment_search", alignment_output, session_id, user_id, inputs)

        return {
            "query": search_query,
            "web_results": web_summary,
            "corpus_answer": corpus_output,
            "alignment_results": alignment_output.get("results", [])
        }