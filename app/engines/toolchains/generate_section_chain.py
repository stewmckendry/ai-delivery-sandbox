from app.tools.tool_wrappers.memory_retrieve import run_tool as memory_retrieve
from app.tools.tool_wrappers.queryCorpus import run_tool as query_corpus
from app.tools.tool_wrappers.goc_alignment_search import Tool as GoCAlignmentTool
from app.tools.tool_wrappers.web_search import run_tool as web_search
from app.tools.tool_wrappers.section_synthesizer import run_tool as synthesize_section


def run_tool(input_dict):
    context = input_dict.get("context", {})
    query = input_dict.get("query")

    memory_results = memory_retrieve({"query": query, "context": context})
    corpus_results = query_corpus({"query": query, "context": context})
    alignment_results = GoCAlignmentTool().run_tool({"query": query, "context": context})
    web_results = web_search({"query": query, "search_type": "general", "context": context})

    synthesis_input = {
        "query": query,
        "context": context,
        "memory": memory_results,
        "corpus_chunks": corpus_results,
        "alignment_results": alignment_results,
        "web_search": web_results
    }

    return synthesize_section(synthesis_input)