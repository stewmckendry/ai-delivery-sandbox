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
        memory = input_dict.get("memory", [])
        corpus_chunks = input_dict.get("corpus_chunks", [])
        alignment_results = input_dict.get("alignment_results", [])
        web_search = input_dict.get("web_search", [])
        corpus_answer = input_dict.get("corpus_answer", {})

        def format_sources(label, entries):
            lines = []
            for entry in entries:
                if isinstance(entry, dict):
                    if "input_summary" in entry and "full_input_path" in entry:
                        lines.append(f"- {entry['input_summary']}: {entry['full_input_path']}")
                    elif "title" in entry and "url" in entry:
                        lines.append(f"- {entry['title']}: {entry['url']}")
                    elif "content" in entry:
                        lines.append(f"- {entry['content'][:200]}...")
                    elif "text" in entry:
                        lines.append(f"- {entry['text'][:200]}...")
            return f"\n{label} Sources:\n" + "\n".join(lines) if lines else ""

        memory_str = format_sources("Project Documentation and Historical Inputs", memory)
        corpus_str = format_sources("Embedded Government Reports and Policies", corpus_chunks)
        alignment_str = format_sources("Government of Canada Strategic Alignment", alignment_results)
        web_str = format_sources("External Web Sources", web_search)
        corpus_answer_str = "\nCorpus-Derived Insight:\n" + corpus_answer.get("answer", "") if corpus_answer else ""

        artifact = input_dict.get("artifact")
        section = input_dict.get("section")

        profile = input_dict.get("project_profile", {})
        profile_context = ""
        if profile:
            profile_context = f"""
[Project Title]
{profile.get('title', 'N/A')}

[Scope Summary]
{profile.get('scope_summary', '')}

[Strategic Alignment]
{profile.get('strategic_alignment', '')}

[Stakeholders]
{profile.get('key_stakeholders', '')}

[Project Type]
{profile.get('project_type', '')}
            """

        prompt = f"""
You are a policy analyst drafting high-quality, evidence-based documents.

Draft a well-structured and dense draft section using all the following inputs.
Focus on clarity, accuracy, and strategic alignment.

Artifact: {artifact}
Section: {section}

[Project Context]
{profile_context}

{memory_str}
{corpus_str}
{corpus_answer_str}
{alignment_str}
{web_str}

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