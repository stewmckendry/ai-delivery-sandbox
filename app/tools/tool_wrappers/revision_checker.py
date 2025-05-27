import logging
from difflib import SequenceMatcher
from app.tools.utils.llm_helpers import chat_completion_request

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        required = ["original_text", "revised_text", "revision_type"]
        for r in required:
            if r not in input_dict:
                raise ValueError(f"Missing required input: {r}")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        orig = input_dict["original_text"]
        revised = input_dict["revised_text"]
        revision_type = input_dict["revision_type"]

        # Heuristic: compute change ratio
        matcher = SequenceMatcher(None, orig.strip(), revised.strip())
        similarity = matcher.ratio()
        change_ratio = 1 - similarity

        flags = []
        if revision_type in ["polish", "targeted_edit"] and change_ratio > 0.3:
            flags.append("high_diff_for_minor_edit")

        # Optional: LLM check for compliance
        messages = [
            {"role": "system", "content": "You evaluate whether an edit followed its instruction."},
            {"role": "user", "content": f"""
Instruction: {revision_type}
Original Text:
{orig}

Revised Text:
{revised}

Did the edit respect the instruction? Reply YES or NO and explain briefly.
"""}]

        response = chat_completion_request(messages, temperature=0.2)

        return {
            "change_ratio": round(change_ratio, 3),
            "flags": flags,
            "llm_verdict": response
        }