import pytest
import sys
import os
import uuid

# Ensure the root of the project is in sys.path so imports like app.tools... work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.toolchains.global_context_chain import GlobalContextChain
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.generate_artifact_chain import GenerateArtifactChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain
from app.tools.tool_wrappers.saveArtifactChunks import Tool as SaveChunksTool
from app.tools.tool_wrappers.fetchArtifactChunk import Tool as FetchArtifactChunk

# Sample IDs
project_id = "test_project"
session_id = "test_session_8aeb34fe-bceb-401d-9c82-68848a89ff22"
artifact_id = "investment_proposal_concept"
gate_id = 0
user_id = "test_user"
section_id = "problem_statement"

sample_text = "This is a sample input for a digital identity project aimed at improving cross-department authentication systems."

@pytest.mark.order(1)
def test_ingest_input():
    chain = IngestInputChain()
    result = chain.run({
        "input_method": "text",
        "text": sample_text,
        "project_id": project_id,
        "metadata": {
            "project_id": project_id,
            "artifact_id": artifact_id,
            "gate_id": gate_id,
            "section_id": section_id,
            "session_id": session_id,
            "user_id": user_id,
            "intent": section_id
        }
    })
    assert result["status"] == "profile_saved"

@pytest.mark.order(2)
def test_global_context_chain():
    result = GlobalContextChain().run({
        "project_id": project_id,
        "session_id": session_id,
        "artifact_id": artifact_id,
        "user_id": user_id
    })
    assert "query" in result and "web_results" in result

@pytest.mark.order(3)
def test_generate_section_chain():
    result = GenerateSectionChain().run({
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact_id": artifact_id,
        "section_id": section_id,
        "project_id": project_id
    })
    assert "raw_draft" in result["final_output"]

@pytest.mark.order(4)
def test_generate_artifact_chain():
    result = GenerateArtifactChain().run({
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact_id": artifact_id,
        "project_id": project_id
    })
    assert "summary" in result and ("sections" in result or "chunks" in result)

@pytest.mark.order(5)
def test_save_artifact_chunks():
    tool = SaveChunksTool()
    result = tool.run_tool({
        "session_id": session_id,
        "artifact_id": artifact_id,
        "gate_id": gate_id,
        "project_id": project_id,
        "max_token": 1000
    })
    assert result["status"] == "success"

@pytest.mark.order(6)
def test_fetch_artifact_chunk():
    tool = FetchArtifactChunk()
    chunk_id = f"problem_statement-chunk1"
    result = tool.run_tool({
        "session_id": session_id,
        "chunk_id": chunk_id
    })
    assert "text" in result

@pytest.mark.order(7)
def test_assemble_artifact_chain():
    chain = AssembleArtifactChain()
    result = chain.run({
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact_id": artifact_id,
        "project_id": project_id
    })
    assert "final_output" in result and "drive_url" in result["final_output"]