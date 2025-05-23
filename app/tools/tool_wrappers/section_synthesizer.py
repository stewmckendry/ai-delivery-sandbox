from app.tools.tool_wrappers.base_tool import Tool
from openai import OpenAI
import os
from app.schemas.section_draft_output import SectionDraftOutput
import re

class SectionSynthesizer(Tool):
    def run_tool(self, inputs):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        memory = inputs.get("memory")
        artifact = inputs.get("artifact")
        section = inputs.get("section")

        prompt = f"""
        Based on the following user-provided inputs, draft a coherent and concise section draft. Keep it focused, factual, and well-structured.

        Artifact: {artifact}
        Section: {section}
        Input Memory:
        {memory}

        Begin the draft below:
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a skilled government proposal writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw_draft = response.choices[0].message.content.strip()
        draft_chunks = re.split(r'\n\n+', raw_draft)  # Split into paragraphs

        return SectionDraftOutput(
            prompt_used=prompt,
            raw_draft=raw_draft,
            draft_chunks=draft_chunks
        ).dict()