import os
import pytest
from pprint import pprint
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from app.engines.toolchains.revise_section_chain import ReviseSectionChain
from app.tools.tool_wrappers.feedback_mapper import Tool as FeedbackMapper
from app.tools.tool_wrappers.feedback_preprocessor import Tool as FeedbackPreprocessor
from app.tools.tool_wrappers.section_rewriter import Tool as SectionRewriter
from app.tools.tool_wrappers.revision_checker import Tool as RevisionChecker
from app.tools.tool_wrappers.manualEditSync import Tool as ManualEdit

@pytest.fixture
def base_inputs():
    return {
        "artifact": "A123",
        "section": "S1",
        "feedback_text": "This section should be more concise. Also clarify the acronym used in the second paragraph.",
        "mode": "rewrite",
        "user_id": "U001",
        "project_id": "P001",
        "gate_id": "G1",
        "session_id": "testsession",
        "sections": [{"section_id": "S1", "text": "This is a test summary of the section text."}]
    }

def print_tool_run(tool_name, inputs, output):
    print(f"\n--- Running {tool_name} ---")
    pprint(inputs)
    print("\nOutput:")
    pprint(output)
    print("--- END ---\n")

def test_feedback_preprocessor():
    tool = FeedbackPreprocessor()
    inputs = {"feedback_text": "Shorten this section. Clarify second paragraph."}
    result = tool.run_tool(inputs)
    print_tool_run("feedback_preprocessor", inputs, result)
    assert "split_feedback" in result

def test_feedback_mapper(base_inputs):
    tool = FeedbackMapper()
    result = tool.run_tool(base_inputs)
    print_tool_run("feedback_mapper", base_inputs, result)
    assert "section_ids" in result

def test_section_rewriter(base_inputs):
    tool = SectionRewriter()
    inputs = {
        "section_id": "S1",
        "feedback": "Make this section more concise.",
        "revision_type": "polish",
        "current_text": "This is a test section that needs improvement. Its test text that is about to be rewritten. It should be more concise and clear.",
    }
    result = tool.run_tool(inputs)
    print_tool_run("section_rewriter", inputs, result)
    assert "draft" in result

def test_revision_checker():
    tool = RevisionChecker()
    inputs = {
        "original_text": "This is a section.",
        "revised_text": "This is a revised section.",
        "revision_type": "polish"
    }
    result = tool.run_tool(inputs)
    print_tool_run("revision_checker", inputs, result)
    assert "change_ratio" in result

def test_manual_edit():
    tool = ManualEdit()
    inputs = {
        "section": "S1",
        "artifact": "A123",
        "user_id": "U001",
        "project_id": "P001",
        "feedback_text": "This is a test section.",
        "session_id": "testsession"
    }
    result = tool.run_tool(inputs)
    print_tool_run("manual_edit_sync", inputs, result)
    assert "status" in result

def test_revise_section_chain(base_inputs):
    chain = ReviseSectionChain()
    result = chain.run(base_inputs)
    print_tool_run("revise_section_chain", base_inputs, result)
    assert "status" in result
    assert result["status"] == "complete"