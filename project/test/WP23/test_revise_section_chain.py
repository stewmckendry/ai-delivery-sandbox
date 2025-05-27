import os
import pytest
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
        "sections": ["S1"]
    }

def test_feedback_preprocessor():
    tool = FeedbackPreprocessor()
    result = tool.run_tool({"feedback_text": "Shorten this section. Clarify second paragraph."})
    assert "split_feedback" in result
    assert isinstance(result["split_feedback"], list)

def test_feedback_mapper(base_inputs):
    tool = FeedbackMapper()
    result = tool.run_tool(base_inputs)
    assert "section_ids" in result

def test_section_rewriter(base_inputs):
    tool = SectionRewriter()
    result = tool.run_tool({
        "section_id": "S1",
        "feedback": "Make this section more concise.",
        "revision_type": "polish",
        "current_text": "This is a test section that needs improvement."
    })
    assert "draft" in result

def test_revision_checker():
    tool = RevisionChecker()
    result = tool.run_tool({
        "original_text": "This is a section.",
        "revised_text": "This is a revised section.",
        "revision_type": "polish"
    })
    assert "change_ratio" in result

def test_manual_edit():
    tool = ManualEdit()
    result = tool.run_tool({
        "section": "S1",
        "artifact": "A123",
        "user_id": "U001",
        "project_id": "P001",
        "feedback_text": "This is a test section.",
        "session_id": "testsession"
    })
    assert "status" in result

def test_revise_section_chain(base_inputs):
    chain = ReviseSectionChain()
    result = chain.run(base_inputs)
    assert "status" in result
    assert result["status"] == "complete"