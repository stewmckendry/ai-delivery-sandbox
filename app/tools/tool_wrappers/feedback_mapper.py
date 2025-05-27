import logging
from app.tools.llm.gpt import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        if "feedback_text" not in input_dict:
            raise ValueError("feedback_text is required")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        feedback = input_dict["feedback_text"]
        artifact = input_dict.get("artifact")
        section = input_dict.get("section")
        project_id = input_dict.get("project_id")

        prompt = f"""
        You are a policy document editor. A user has submitted feedback on a public sector program artifact.

        Analyze the following feedback and return:
        - A list of section IDs affected (if specified, prioritize that section)
        - The type of revision required: rewrite, polish, append, or clarify

        Feedback:
        ---
        {feedback}
        ---
        
        Respond in JSON format:
        {{
          "section_ids": [...],
          "revision_type": "..."
        }}
        """

        response = chat_completion_request(
            messages=[{"role": "system", "content": "You help map feedback to document revisions."},
                      {"role": "user", "content": prompt}],
            temperature=0.2
        )

        try:
            parsed = eval(response["content"].strip())
            logger.info(f"Parsed feedback map: {parsed}")
            return parsed
        except Exception as e:
            logger.error("Failed to parse LLM response", exc_info=e)
            return {"section_ids": [section] if section else [], "revision_type": "rewrite", "llm_response": response["content"]}