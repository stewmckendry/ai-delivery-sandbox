import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from app.schemas.section_draft_output import SectionDraftOutput

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "raw_draft" not in input_dict:
            raise ValueError("Missing required field: raw_draft")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        raw_draft = input_dict["raw_draft"]

        prompt = f"""
        Please refine the following draft for clarity, tone, and grammar.
        Keep the structure and meaning, but improve readability and polish.

        Draft:
        {raw_draft}
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a writing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        refined_draft = response.choices[0].message.content.strip()
        draft_chunks = re.split(r'\n\n+', refined_draft)

        return SectionDraftOutput(
            prompt_used=prompt,
            raw_draft=refined_draft,
            draft_chunks=draft_chunks
        ).dict()