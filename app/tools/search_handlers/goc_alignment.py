from app.tools.tool_utils.search_api_utils import bing_web_search
from app.engines.memory_sync import log_tool_usage

def handle_goc_alignment_search(inputs: dict = None) -> list:
    """
    Executes a government-aligned web search restricted to .gc.ca domains.
    Example: query='open government strategy' -> search: 'open government strategy site:.gc.ca'
    """
    query = inputs.get("query")
    scoped_query = f"{query} site:.gc.ca"

    alignment_output = bing_web_search(scoped_query)

    # Log the search results to PromptLog for use in section generation
    log_tool_usage("goc_alignment_search", "global_context | goc_alignment_search", alignment_output, inputs.get("session_id"), inputs.get("user_id"), inputs)

    return alignment_output