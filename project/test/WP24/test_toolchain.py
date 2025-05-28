import pytest
from app.tools.tool_wrappers.query_prompt_generator import Tool as QueryPromptTool
from app.tools.tool_wrappers.section_synthesizer import Tool as SynthTool
from app.tools.tool_wrappers.section_refiner import Tool as RefineTool
from app.tools.tool_wrappers.refine_document_chain import Tool as RefineDocTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain

@pytest.fixture
def test_context():
    return {
        "project_profile": {
            "title": "AI Ethics Policy",
            "scope_summary": "Create a federal guideline on ethical AI use",
            "strategic_alignment": "Supports digital innovation mandate",
            "key_stakeholders": "Treasury Board, ISED",
            "project_type": "Policy Development",
            "project_id": "proj-test-123"
        },
        "memory": [
            {"input_summary": "Summary of past AI policy", "full_input_path": "/mem/ai_policy_2021.txt"},
            {"text": "AI ethics requires transparency and fairness."}
        ]
    }

def test_query_prompt_generator(test_context):
    tool = QueryPromptTool()
    output = tool.run_tool({"project_profile": test_context["project_profile"], "memory": test_context["memory"]})
    assert "query" in output and isinstance(output["query"], str)

def test_section_synthesizer(test_context):
    tool = SynthTool()
    output = tool.run_tool({
        "artifact": "AI Ethics",
        "section": "Transparency",
        "project_profile": test_context["project_profile"],
        "memory": test_context["memory"],
        "corpus_answer": {"answer": "Transparency is a core principle."},
        "alignment_results": [],
        "web_search": "AI transparency efforts are underway globally."
    })
    assert "raw_draft" in output
    return output["raw_draft"]

def test_section_refiner(test_section_synthesizer):
    tool = RefineTool()
    output = tool.run_tool({"raw_draft": test_section_synthesizer})
    assert "raw_draft" in output


def test_refine_document_chain():
    long_text = "\n\n".join([f"Paragraph {i}: Detail on AI governance." for i in range(30)])
    tool = RefineDocTool()
    output = tool.run_tool({"document_body": long_text})
    assert "refined_body" in output


def test_generate_section_chain(test_context):
    chain = GenerateSectionChain()
    output = chain.run({
        "artifact": "AI Ethics",
        "section": "Transparency",
        "project_profile": test_context["project_profile"],
        "context_summary": "Focus on risks of unexplainable models.",
        "user_id": "user-test-1",
        "session_id": "sess-test-1"
    })
    assert "final_output" in output and "trace" in output


def test_assemble_artifact_chain(test_context):
    chain = AssembleArtifactChain()
    output = chain.run({
        "artifact": "AI Ethics",
        "gate_id": "0",
        "project_profile": test_context["project_profile"],
        "user_id": "user-test-1",
        "session_id": "sess-test-1"
    })
    assert "markdown" in output