from app.engines.base_toolchain import BaseToolchain
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import log_tool_usage

class Toolchain(BaseToolchain):
    def run(self, inputs: dict) -> dict:
        self.log_info("[Chain] Starting generate_global_context_chain")

        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        project_id = inputs.get("project_id")
        gate_id = inputs.get("gate_id")
        artifact = inputs.get("artifact")
        section = inputs.get("section")
        project_profile = inputs.get("project_profile")
        memory = inputs.get("memory", [])

        query_prompt_tool = ToolRegistry().get_tool("query_prompt_generator")
        query_prompt_inputs = {"project_profile": project_profile, "memory": memory}
        query_result = query_prompt_tool.run_tool(query_prompt_inputs)
        query = query_result.get("query")
        self.log_info(f"[Chain] Generated query: {query}")

        context = {
            "session_id": session_id,
            "user_id": user_id,
            "project_id": project_id,
            "gate_id": gate_id,
            "artifact": artifact,
            "section": section,
            "project_profile": project_profile
        }

        web_tool = ToolRegistry().get_tool("webSearch")
        web_result = web_tool.run_tool({"query": query, "context": context})
        log_tool_usage(tool_name="webSearch", input_summary="global_context | webSearch", output_summary=web_result, metadata=inputs)

        corpus_tool = ToolRegistry().get_tool("queryCorpus")
        corpus_result = corpus_tool.run_tool({"query": query, "context": context})
        log_tool_usage(tool_name="queryCorpus", input_summary="global_context | queryCorpus", output_summary=corpus_result, metadata=inputs)

        alignment_tool = ToolRegistry().get_tool("goc_alignment_search")
        alignment_result = alignment_tool.run_tool({"query": query, "context": context})
        log_tool_usage(tool_name="goc_alignment_search", input_summary="global_context | goc_alignment_search", output_summary=alignment_result, metadata=inputs)

        self.log_info("[Chain] generate_global_context_chain complete")

        return {
            "query": query,
            "web_search": web_result,
            "corpus_answer": corpus_result,
            "alignment_results": alignment_result
        }