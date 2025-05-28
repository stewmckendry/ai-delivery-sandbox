# Patch script to apply runtime validation to all tool wrappers

from .compose_and_cite import Tool as ComposeAndCite
from .searchKnowledgeBase import Tool as SearchKnowledgeBase
from .externalWebSearch import Tool as ExternalWebSearch
from .composeDraft import Tool as ComposeDraft
from .validateSection import Tool as ValidateSection
from .logReasoningTrace import Tool as LogReasoningTrace
from .commitDocument import Tool as CommitDocument
from .fetchDocument import Tool as FetchDocument
from .getTokenUsage import Tool as GetTokenUsage
from .queryAirtable import Tool as QueryAirtable
from .parseTranscript import Tool as ParseTranscript
from .loadCorpus import Tool as LoadCorpus
from .doc_feedback_to_task import Tool as DocFeedbackToTask
from .diff_and_summarize_sections import Tool as DiffAndSummarizeSections
from .submitDocumentFeedback import Tool as SubmitDocumentFeedback
from .summarize_feedback_log import Tool as SummarizeFeedbackLog

# These wrappers already updated: commitSection, translateDocument

# Example pattern added to each tool
# def run_tool(self, input_dict):
#     self.validate(input_dict)
#     return {"status": "not_implemented", "tool": "tool_name"}

# Note: validation hook is dynamically injected from tool_registry.py
# Tool wrappers are kept minimal
