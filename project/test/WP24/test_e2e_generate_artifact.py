import pytest
from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.toolchains.generate_full_artifact_chain import GenerateFullArtifactChain
from app.models.artifact import Artifact

@pytest.mark.skipif(True, reason="Run manually to avoid accidental test data upload")
def test_e2e_generate_artifact():
    project_id = "demo-project-1"
    artifact_id = "A1"
    input_path = "test_data/demo_input.txt"

    print("--- Step 1: Ingest Input ---")
    ingest_tool = IngestInputChain()
    ingest_result = ingest_tool.run({
        "project_id": project_id,
        "path": input_path
    })
    print("Ingest Output:", ingest_result)

    print("--- Step 2: Generate Full Artifact ---")
    gen_tool = GenerateFullArtifactChain()
    output = gen_tool.run({
        "project_id": project_id,
        "artifact": artifact_id,
        "session_id": "s-test",
        "user_id": "test-user"
    })
    print("Final Output:", output["final_output"])
    for step in output["trace"]:
        print("\nTool:", step["tool"])
        print("Output:", step["output"])