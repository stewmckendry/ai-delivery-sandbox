import logging
from app.tools.utils.llm_helpers import chat_completion_request
from app.tools.utils.section_helpers import get_token_count

logger = logging.getLogger(__name__)

class RefineDocumentChain:
    def __init__(self):
        self.token_limit = 7000  # buffer below 8k context

    def run(self, document_body, title=None, project_id=None):
        if get_token_count(document_body) > self.token_limit:
            logger.warning("Document too long for safe refinement – skipping.")
            return {"refined_body": document_body, "skipped": True}

        system_prompt = """
You are a policy writing assistant. Polish the following draft document for consistency, tone, clarity, and logical flow.
Avoid making substantive changes to facts or content – improve structure and coherence only.
Preserve all key content and section headings. Return the polished version in markdown format.
"""

        user_prompt = f"""
Title: {title or "Policy Document"}

---

{document_body}
"""

        response = chat_completion_request(
            system=system_prompt.strip(),
            user=user_prompt.strip()
        )

        return {"refined_body": response.strip(), "skipped": False}