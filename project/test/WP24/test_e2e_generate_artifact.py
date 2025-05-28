import pytest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.toolchains.generate_full_artifact_chain import GenerateFullArtifactChain

@pytest.mark.skipif(False, reason="Run manually to avoid accidental test data upload")
def test_e2e_generate_artifact():
    project_id = "demo-project-1"
    artifact_id = "investment_proposal_concept"
    input_path = "project/test/WP23/test_data/demo_input.txt"
    input_method = "file"  # Can be 'text', 'file', or 'link'

    print("--- Step 1: Ingest Input ---")
    ingest_tool = IngestInputChain()
    ingest_result = ingest_tool.run({
        "project_id": project_id,
        "file_path": input_path,
        "input_method": input_method
    })
    print("Ingest Output:", ingest_result)

    print("--- Step 2: Generate Full Artifact ---")
    gen_tool = GenerateFullArtifactChain()
    output = gen_tool.run({
        "project_id": project_id,
        "artifact_id": artifact_id,
        "session_id": "s-test",
        "user_id": "test-user",
        "gate_id": "0"  # Assuming gate_id is required
    })
    print("Final Output:", output["final_output"])
    for step in output["trace"]:
        print("\nTool:", step["tool"])
        print("Output:", step["output"])