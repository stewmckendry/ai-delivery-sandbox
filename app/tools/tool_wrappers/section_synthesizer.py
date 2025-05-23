import os
import openai

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

        prompt = f"""
        Based on the following user-provided inputs, draft a coherent and concise section draft. Keep it focused, factual, and well-structured.

        Context:
        {context_str}

        Begin the draft below:
        """

        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a policy analyst drafting high-quality documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return {
            "prompt_used": prompt,
            "raw_draft": response.choices[0].message["content"].strip()
        }