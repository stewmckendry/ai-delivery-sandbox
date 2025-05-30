"""
Test Script: test_iteration_4.py
Purpose: Executes each step in the PolicyGPT UX flow to validate tool and chain integration.
Log Format: Prints inputs, outputs, and status for each step. Reuses shared metadata.
"""

import sys, os
import pytest
from pathlib import Path

# Tool and chain imports
from app.tools.tool_wrappers.inputPromptGenerator import Tool as PromptGen
from app.tools.tool_wrappers.record_research import Tool as ResearchTool
from app.tools.tool_wrappers.section_review_feedback import Tool as FeedbackTool
from app.tools.tool_wrappers.section_review_fetcher import Tool as FetchReviewTool
from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.revise_section_chain import ReviseSectionChain
from app.engines.toolchains.global_context_chain import GlobalContextChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain

# --- Configurable test values ---
project_id = "test_policy_project"
session_id = "test_session_042"
user_id = "user_admin"
gate_id = 3
artifact = "investment_proposal_concept"
section = "problem_context"

@pytest.fixture(scope="module")
def shared_state():
    return {
        "project_id": project_id,
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact": artifact,
        "section": section,
        "stub_profile": {
            "name": "Digital Identity Modernization",
            "description": "Unifying digital identity efforts across departments.",
            "program_context": "Cross-government initiative targeting trust and usability."
        }
    }

def test_1_prompt_generation(shared_state):
    out = PromptGen().run_tool({
        "section_id": shared_state['section'],
        "artifact_id": shared_state['artifact'],
        "gate_id": shared_state['gate_id']
    })
    print("Prompt Output:", out)

def test_2_ingest_input(shared_state):
    raw_text = "This is a test input for the problem context section."
    result = IngestInputChain().run({
        "text": raw_text,
        **shared_state
    })
    print("Ingest Result:", result)

def test_3_record_research(shared_state):
    out = ResearchTool().run_tool({
        **shared_state,
        "note": "Relevant context from gov-wide digital strategy."
    })
    print("Research Recorded:", out)

def test_4_generate_section(shared_state):
    out = GenerateSectionChain().run({
        **shared_state,
        "project_profile": shared_state["stub_profile"]
    })
    print("Draft Output:\n", out["final_output"]["raw_draft"])

def test_5_feedback(shared_state):
    draft_text = "Initial draft for testing feedback."
    out = FeedbackTool().run_tool({
        "text": draft_text,
        "goals": ["clarity", "alignment"]
    })
    print("Feedback:", out)

def test_6_revise(shared_state):
    out = ReviseSectionChain().run({
        **shared_state,
        "feedback": ["Clarify objective"],
        "prior_draft": "Initial draft for testing feedback."
    })
    print("Revised Draft:\n", out["revised_text"])

def test_7_fetch_review(shared_state):
    out = FetchReviewTool().run_tool({
        "session_id": shared_state["session_id"],
        "section_id": shared_state["section"]
    })
    print("Fetched Review State:", out)

def test_8_global_context(shared_state):
    out = GlobalContextChain().run({
        **shared_state
    })
    print("Global Context Summary:", out["summary"])

def test_9_assemble_artifact(shared_state):
    out = AssembleArtifactChain().run({
        **shared_state
    })
    print("Final Artifact URL:", out["drive_url"])
