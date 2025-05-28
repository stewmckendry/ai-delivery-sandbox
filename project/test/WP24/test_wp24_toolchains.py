import pytest
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.generate_full_artifact_chain import GenerateFullArtifactChain

@pytest.mark.parametrize("inputs", [
    {
        "artifact": "sample_artifact_001",
        "section": "sample_section_001",
        "project_id": "proj_001",
        "user_id": "test_user",
        "session_id": "test_session_001",
        "gate_id": "gate1",
        "context_summary": "This section builds upon prior analysis on community impact."
    }
])
def test_generate_section_chain(inputs):
    tool = GenerateSectionChain()
    result = tool.run(inputs)
    assert result["final_output"].get("raw_draft"), "Expected raw draft output"
    assert "trace" in result, "Trace output missing"

def test_generate_full_artifact_chain():
    tool = GenerateFullArtifactChain()
    output = tool.run(
        artifact_id="sample_artifact_001",
        gate_id="gate1",
        project_id="proj_001",
        user_id="test_user"
    )
    assert "session_id" in output, "Session ID missing in output"
    assert "drive_link" in output, "Drive link missing in final output"
