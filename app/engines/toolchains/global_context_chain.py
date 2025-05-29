import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage

logger = logging.getLogger(__name__)

class GlobalContextChain:
    def __init__(self):
        registry = ToolRegistry()
        self.web_search_tool = registry.get_tool("webSearch")
        self.query_tool = registry.get_tool("query_prompt_generator")
        self.corpus_tool = registry.get_tool("queryCorpus")
        self.alignment_tool = registry.get_tool("goc_alignment_search")

    def run(self, inputs):
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        context = inputs.get("context", {})

        # Step 1: Generate a smart search query
        query_payload = {
            "project_profile": context.get("project_profile", {}),
            "memory": context.get("memory", [])
        }
        query_output = self.query_tool.run_tool(query_payload)
        search_query = query_output.get("query")
        log_tool_usage("queryPromptGenerator", "global_context | query_prompt_generator", query_output, session_id, user_id, inputs)

        # Step 2: Web Search
        web_results = self.web_search_tool.run_tool({
            "query": search_query,
            "search_type": "general",
            "context": context
        })
        log_tool_usage("webSearch", "global_context | webSearch", web_results, session_id, user_id, inputs)

        # Step 3: Embedded Corpus Search
        corpus_output = self.corpus_tool.run_tool({
            "query": search_query,
            "context": context,
            "memory": context.get("memory", [])
        })
        log_tool_usage("queryCorpus", "global_context | queryCorpus", corpus_output, session_id, user_id, inputs)

        # Step 4: GoC Alignment
        alignment_output = self.alignment_tool.run_tool({
            "query": search_query,
            "context": context,
            "memory": context.get("memory", [])
        })
        log_tool_usage("goc_alignment_search", "global_context | goc_alignment_search", alignment_output, session_id, user_id, inputs)

        return {
            "query": search_query,
            "web_results": web_results,
            "corpus_answer": corpus_output,
            "alignment_results": alignment_output.get("results", [])
        }