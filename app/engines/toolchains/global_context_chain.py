import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage
from app.engines.project_profile_engine import ProjectProfileEngine
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template
from app.db.models.PromptLog import PromptLog  # inline import to avoid circular dependency
from app.db.database import SessionLocal
from sqlalchemy import and_

logger = logging.getLogger(__name__)

class GlobalContextChain:
    def __init__(self):
        registry = ToolRegistry()
        self.web_search_tool = registry.get_tool("webSearch")
        self.query_tool = registry.get_tool("query_prompt_generator")
        self.corpus_tool = registry.get_tool("alignWithReferenceDocuments")
        self.alignment_tool = registry.get_tool("goc_alignment_search")
        self.memory_tool = registry.get_tool("memory_retrieve")
    
    def summarize_web_results(self, search_results):
        if not search_results:
            logger.info("[global_context] No web search results provided")
            return ""

        snippets = "\n".join([
            f"{entry['title']}: {entry['snippet']}"
            for entry in search_results if 'title' in entry and 'snippet' in entry
        ])

        if not snippets.strip():
            logger.info("[global_context] No usable title/snippet pairs found in web search results")
            return ""

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
                PromptLog.tool.in_(["queryCorpus", "record_research"])
            )
        ).all()

        if not results:
            return {}

        grouped_context = {"Reference Document Alignment": [], "Web Search": []}
        seen_outputs = {"Reference Document Alignment": set(), "Web Search": set()}

        for log in results:
            label = "Reference Document Alignment" if log.tool == "queryCorpus" else "Web Search"
            output = log.output_summary

            if output and output not in seen_outputs[label]:
                grouped_context[label].append(output)
                seen_outputs[label].add(output)

        return grouped_context

    def summarize_global_context(self, grouped_context):
        # Exit early if there's no context to summarize
        if not grouped_context or all(not items for items in grouped_context.values()):
            return ""

        def format_context_group(group):
            formatted = []
            for item in group:
                if isinstance(item, dict):
                    citation = item.get("title") or "Untitled"
                    source = item.get("source", "Unknown Source")
                    date = item.get("date", "n.d.")
                    url = item.get("url", "")
                    summary = item.get("snippet") or item.get("text") or item
                    formatted.append(f"- {summary}\n  (Source: \"{citation}\", {source}, {date}, {url})")
                else:
                    formatted.append(f"- {item}")
            return "\n".join(formatted)

        formatted_contexts = {
            label: format_context_group(items) for label, items in grouped_context.items() if items
        }

        if not formatted_contexts:
            return ""

        prompt_templates = get_prompt("generate_section_prompts.yaml", "global_context_synthesis")
        system_prompt = Template(prompt_templates["system"]).render()
        user_prompt = Template(prompt_templates["user"]).render(contexts=formatted_contexts)
        return chat_completion_request(system_prompt, user_prompt, temperature=0.3)


    def run(self, inputs):
        logger.info("[GlobalContextChain] Starting global context chain")
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        artifact_id = inputs.get("artifact_id")
        project_id = inputs.get("project_id")
        search_filter = inputs.get("search_filter", {}) # used in web_search for jurisdiction and market searches

        memory = self.memory_tool.run_tool({
            "artifact_id": artifact_id,
            "project_id": project_id,
            "session_id": session_id,
            "user_id": user_id
        })
        logger.info(f"[GlobalContextChain] Retrieved memory for artifact {artifact_id} in project {project_id}")
        log_tool_usage("memory_retrieve", "memory_retrieve", memory, session_id, user_id, inputs)

        profile_engine = ProjectProfileEngine()
        project_profile = profile_engine.load_profile(project_id)
        logger.info(f"[GlobalContextChain] Loaded project profile for project {project_id}. Profile data: {project_profile}")
        log_tool_usage("project_profile", "project_profile", project_profile, session_id, user_id, inputs)

        # Step 1: Generate a smart search query
        query_payload = self.query_tool.run_tool({
            "project_profile": project_profile,
            "memory": memory
        })
        search_query = query_payload.get("query")
        logger.info(f"[GlobalContextChain] Generated search query: {search_query}")
        log_tool_usage("queryPromptGenerator", "query_prompt_generator", query_payload, session_id, user_id, inputs)

        # Step 2: Web Search
        input_dict = {**inputs, **search_filter}
        web_results = self.web_search_tool.run_tool({
            "query": search_query,
            "search_type": "general",
            "input_dict": input_dict
        })
        web_summary = self.summarize_web_results(web_results)
        logger.info(f"[GlobalContextChain] Retrieved web search results for query: {search_query}")

        # Step 3: Embedded Corpus Search
        input_dict = {**inputs, "query": search_query}
        corpus_output = self.corpus_tool.run_tool({
            "input_dict": input_dict
        })
        logger.info(f"[GlobalContextChain] Retrieved corpus search results for query: {search_query}")

        # Step 4: GoC Alignment
        alignment_output = self.alignment_tool.run_tool({
            "input_dict": input_dict
        })
        logger.info(f"[GlobalContextChain] Retrieved alignment results: {alignment_output}")

        logger.info("[GlobalContextChain] Summarizing global context complete")
        return {
            "query": search_query,
            "web_results": web_summary,
            "corpus_answer": corpus_output,
            "alignment_results": alignment_output.get("results", [])
        }