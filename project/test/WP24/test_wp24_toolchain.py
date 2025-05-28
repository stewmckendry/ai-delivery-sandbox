import os
import pytest
from app.tools.tool_wrappers.query_prompt_generator import Tool as QueryPromptTool
from app.tools.tool_wrappers.section_synthesizer import Tool as SynthTool
from app.tools.tool_wrappers.section_refiner import Tool as RefineTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain

def base_inputs():
    return {
        "project_profile": {
            "title": "Test Project",
            "scope_summary": "Scope description.",
            "strategic_alignment": "Alignment info.",
            "key_stakeholders": "Stakeholder list",
            "project_type": "Type A",
            "project_id": "test-project-001"
        },
        "memory": [
            {"input_summary": "Historical doc A"},
            {"text": "Some text extract."}
        ],
        "artifact": "Test Artifact",
        "section": "Test Section",
        "user_id": "user001",
        "session_id": "sess001",
        "gate_id": "gate00",
        "context_summary": "Optional context summary."
    }


def test_query_prompt_generator():
    tool = QueryPromptTool()
    inputs = base_inputs()
    result = tool.run_tool({"project_profile": inputs["project_profile"], "memory": inputs["memory"]})
    print("[query_prompt_generator] Result:", result)
    assert "query" in result


def test_section_synthesizer():
    tool = SynthTool()
    inputs = base_inputs()
    structured_inputs = {
        "memory": inputs["memory"],
        "web_search": "Summary of web search.",
        "corpus_answer": {"answer": "Corpus-based answer."},
        "alignment_results": [],
        "context_summary": inputs["context_summary"]
    }
    result = tool.run_tool({**inputs, **structured_inputs})
    print("[section_synthesizer] Result:", result)
    assert "raw_draft" in result


def test_section_refiner():
    tool = RefineTool()
    result = tool.run_tool({"raw_draft": "This is a raw draft for testing refinement."})
    print("[section_refiner] Result:", result)
    assert "raw_draft" in result


def test_generate_section_chain():
    tool = GenerateSectionChain()
    inputs = base_inputs()
    result = tool.run(inputs)
    print("[generate_section_chain] Trace:", [step['tool'] for step in result["trace"]])
    assert "final_output" in result
    assert "save_result" in result