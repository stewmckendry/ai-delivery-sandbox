from app.engines.base_toolchain import BaseToolchain
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

class GenerateGlobalContextChain(BaseToolchain):
    def __init__(self):
        super().__init__()
        registry = ToolRegistry()
        self.query_tool = registry.get_tool("query_prompt_generator")
        self.web_tool = registry.get_tool("webSearch")
        self.corpus_tool = registry.get_tool("queryCorpus")
        self.align_tool = registry.get_tool("goc_alignment_search")

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
        return chat_completion_request(system_prompt, user_prompt, temperature=0.3)

    def run(self, inputs):
        trace = []
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")

        memory = inputs.get("memory")
        project_profile = inputs.get("project_profile")

        query = self.query_tool.run_tool({"project_profile": project_profile, "memory": memory})
        log_tool_usage("queryPromptGenerator", "global_context | queryPromptGenerator", query, session_id, user_id, inputs)
        trace.append({"tool": "queryPromptGenerator", "output": query})

        web = self.web_tool.run_tool({"query": query["query"], "context": inputs, "memory": memory})
        summary = self.summarize_web_results(web)
        log_tool_usage("web_search", "global_context | web_search", web, session_id, user_id, inputs)
        trace.append({"tool": "web_search", "output": web})

        corpus = self.corpus_tool.run_tool({"query": query["query"], "context": inputs, "memory": memory})
        log_tool_usage("queryCorpus", "global_context | queryCorpus", corpus, session_id, user_id, inputs)
        trace.append({"tool": "queryCorpus", "output": corpus})

        align = self.align_tool.run_tool({"query": query["query"], "context": inputs, "memory": memory})
        results = align.get("results", [])
        log_tool_usage("goc_alignment_search", "global_context | goc_alignment_search", results, session_id, user_id, inputs)
        trace.append({"tool": "goc_alignment_search", "output": results})

        return {
            "trace": trace,
            "global_context": {
                "web_search": summary,
                "corpus_answer": corpus,
                "alignment_results": results
            }
        }