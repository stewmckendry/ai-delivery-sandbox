import logging
import uuid
import os
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage
from app.tools.utils.llm_helpers import chat_completion_request, get_prompt
from jinja2 import Template

logger = logging.getLogger(__name__)

class GenerateSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.query_tool = registry.get_tool("queryPromptGenerator")
        self.corpus_tool = registry.get_tool("queryCorpus")
        self.alignment_tool = registry.get_tool("goc_alignment_search")
        self.synth_tool = registry.get_tool("section_synthesizer")
        self.refine_tool = registry.get_tool("section_refiner")
        self.web_search_tool = registry.get_tool("webSearch")

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
        artifact_id = inputs.get("artifact")
        section_id = inputs.get('section')
        gate_id = inputs.get("gate_id", "0")
        project_id = inputs.get("project_id") or inputs.get("project_profile", {}).get("project_id")

        context_summary = inputs.get("context_summary", "")
        log_tool_usage("context_summary", "context summary input", context_summary, session_id, user_id, inputs)

        memory_input = {**inputs}
        if "project_profile" in inputs:
            memory_input["project_profile"] = inputs["project_profile"]

        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        search_results = self.web_search_tool.run_tool({
            "query": f"{inputs.get('artifact')} - {inputs.get('section')}",
            "search_type": "general",
            "context": {"project_profile": inputs.get("project_profile", {})}
        })
        log_tool_usage("web_search", "external scan", search_results, session_id, user_id, inputs)
        trace.append({"tool": "web_search", "output": search_results})
        logger.info("[Step 2] web_search complete")

        web_summary = self.summarize_web_results(search_results)

        query = self.query_tool.run_tool({
            "project_profile": inputs.get("project_profile", {}),
            "memory": memory
        })
        log_tool_usage("queryPromptGenerator", "generated search query", query, session_id, user_id, inputs)
        trace.append({"tool": "queryPromptGenerator", "output": query})
        logger.info("[Step 3] query_prompt_generator complete")

        corpus_results = self.corpus_tool.run_tool({
            "query": query["query"],
            "context": inputs,
            "memory": memory
        })
        log_tool_usage("queryCorpus", "embedded corpus scan", corpus_results, session_id, user_id, inputs)
        trace.append({"tool": "queryCorpus", "output": corpus_results})
        logger.info("[Step 4] queryCorpus complete")

        alignment_results = self.alignment_tool.run_tool({
            "query": query["query"],
            "context": inputs,
            "memory": memory
        })
        log_tool_usage("goc_alignment_search", "gc.ca alignment", alignment_results, session_id, user_id, inputs)
        trace.append({"tool": "goc_alignment_search", "output": alignment_results})
        logger.info("[Step 5] goc_alignment_search complete")

        structured_inputs = {
            "memory": memory,
            "web_search": web_summary,
            "corpus_answer": corpus_results,
            "alignment_results": alignment_results,
            "context_summary": context_summary
        }

        draft = self.synth_tool.run_tool({**inputs, **structured_inputs})
        log_tool_usage("section_synthesizer", "generated draft", draft, session_id, user_id, inputs)
        trace.append({"tool": "section_synthesizer", "output": draft})
        logger.info("[Step 6] section_synthesizer complete")

        refined = self.refine_tool.run_tool({**inputs, "raw_draft": draft["raw_draft"]})
        log_tool_usage("section_refiner", "refined draft", refined, session_id, user_id, inputs)
        trace.append({"tool": "section_refiner", "output": refined})
        logger.info("[Step 7] section_refiner complete")

        save_result = save_artifact_and_trace(
            section_id=section_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            text=refined["raw_draft"],
            sources=draft.get("prompt_used"),
            tool_outputs=trace,
            user_id=user_id,
            project_id=project_id
        )
        logger.info("[Step 8] Saved to ArtifactSection and ReasoningTrace")

        return {"final_output": refined, "trace": trace, "save_result": save_result}