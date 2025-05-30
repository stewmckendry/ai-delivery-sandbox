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
project_id = "test_project_6"
session_id = "test_session_qwerty2"
artifact_id = "investment_proposal_concept"
gate_id = 0
user_id = "test_user"
section_id = "problem_statement"

sample_text = (
    "Canadian cities are facing increasing climate risks such as heatwaves, flooding, and air pollution. "
    "Urban green infrastructure (UGI) — including parks, green roofs, rain gardens, and tree canopies — "
    "offers a resilient approach to mitigate these risks. Studies highlight how UGI enhances stormwater management, "
    "lowers urban temperatures, and improves public health (Toronto Environment Office, 2022; Green Cities Canada, 2023).\n\n"
    "Jurisdictions like Vancouver and Montreal are investing heavily in UGI to meet climate targets and improve quality of life. "
    "Federal policies such as the Pan-Canadian Framework on Clean Growth and Climate Change encourage municipalities to integrate "
    "green infrastructure in long-term planning. Moreover, interdisciplinary research suggests that equitable access to UGI contributes "
    "to social resilience, particularly in low-income neighborhoods (McArthur & Stewart, 2021).\n\n"
    "Investment in UGI should prioritize high-risk urban areas, align with community engagement strategies, and leverage both public and "
    "private funding. As climate pressures intensify, embedding green infrastructure within urban planning is essential for sustainable and inclusive adaptation."
)

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