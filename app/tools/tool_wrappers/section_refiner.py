import os
from openai import OpenAI

class Tool:
    def validate(self, input_dict):
        if "raw_draft" not in input_dict:
            raise ValueError("Missing required field: raw_draft")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        raw_draft = input_dict["raw_draft"]

        prompt = f"""
        Refine the following draft to ensure clear structure, concise language, and professional tone. Fix grammar, eliminate repetition, and improve readability.

        Draft:
        {raw_draft}

        Refined Version:
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert editor for government documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        return {
            "prompt_used": prompt,
            "refined_draft": response.choices[0].message.content.strip()
        }