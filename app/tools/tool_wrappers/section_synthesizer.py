import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from app.schemas.section_draft_output import SectionDraftOutput

load_dotenv()

class Tool:
    def validate(self, input_dict):
        if "memory" not in input_dict:
            raise ValueError("Missing required field: memory")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        memory = input_dict["memory"]
        context_str = "\n".join([
            f"- {entry['input_summary']}: {entry['full_input_path']}"
            for entry in memory
        ])

        artifact = input_dict.get("artifact")
        section = input_dict.get("section")

        prompt = f"""
        Based on the following user-provided inputs, draft a coherent and concise section draft. Keep it focused, factual, and well-structured.

        Artifact: {artifact}
        Section: {section}
        Context:
        {context_str}

        Begin the draft below:
        """

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a policy analyst drafting high-quality documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw_draft = response.choices[0].message.content.strip()
        draft_chunks = re.split(r'\n\n+', raw_draft)

        return SectionDraftOutput(
            prompt_used=prompt,
            raw_draft=raw_draft,
            draft_chunks=draft_chunks
        ).dict()