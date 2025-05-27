import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "raw_draft" not in input_dict:
            raise ValueError("Missing required field: raw_draft")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        raw_draft = input_dict.get("raw_draft")

        prompt = f"""
You are a policy analyst. Polish the following draft for clarity, coherence, and professional tone. Do not change the core content or structure unless clarity demands it.

Draft:
{raw_draft}
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        refined = response.choices[0].message.content.strip()
        return {"raw_draft": refined, "prompt_used": prompt}