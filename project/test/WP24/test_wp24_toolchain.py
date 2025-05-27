import os
import logging
from app.tools.tool_wrappers.query_prompt_generator import Tool as QueryPromptTool
from app.tools.tool_wrappers.section_synthesizer import Tool as SynthTool
from app.tools.tool_wrappers.section_refiner import Tool as RefineTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock inputs
project_profile = {
    "title": "Test Project",
    "scope_summary": "Scope description.",
    "strategic_alignment": "Alignment info.",
    "key_stakeholders": "Stakeholder list",
    "project_type": "Type A",
    "project_id": "test-project-001"
}

memory = [{"input_summary": "Historical doc A"}, {"text": "Some text extract."}]
raw_draft = "This is a raw draft for testing refinement."

artifact_id = "artifact123"
section_id = "sectionABC"
user_id = "user001"
session_id = "sess001"
gate_id = "gate00"

# --- Unit Tests ---
print("\n[Test] query_prompt_generator")
query_tool = QueryPromptTool()
query_output = query_tool.run_tool({"project_profile": project_profile, "memory": memory})
print("Output:", query_output)

print("\n[Test] section_synthesizer")
synth_tool = SynthTool()
synth_output = synth_tool.run_tool({
    "project_profile": project_profile,
    "artifact": "Test Artifact",
    "section": "Test Section",
    "memory": memory,
    "alignment_results": [],
    "web_search": "Summary of web search.",
    "corpus_answer": {"answer": "Corpus-based answer."},
    "context_summary": "Optional context summary."
})
print("Output:", synth_output)

print("\n[Test] section_refiner")
refine_tool = RefineTool()
refine_output = refine_tool.run_tool({"raw_draft": raw_draft})
print("Output:", refine_output)

# --- End-to-End Chain Test ---
print("\n[Test] generate_section_chain")
chain = GenerateSectionChain()
full_output = chain.run({
    "project_profile": project_profile,
    "artifact": "Test Artifact",
    "section": "Test Section",
    "user_id": user_id,
    "session_id": session_id,
    "project_id": project_profile["project_id"],
    "gate_id": gate_id
})
print("Trace steps:", [step['tool'] for step in full_output["trace"]])
print("Final output saved:", full_output["save_result"])

# Note: Regression test for generate_artifact_chain assumed separately covered in WP23 tests