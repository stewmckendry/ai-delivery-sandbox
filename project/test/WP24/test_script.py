import json
from app.tools.tool_wrappers.query_prompt_generator import Tool as QueryPromptTool
from app.tools.tool_wrappers.section_synthesizer import Tool as SynthTool
from app.tools.tool_wrappers.section_refiner import Tool as RefineTool
from app.tools.tool_wrappers.refine_document_chain import Tool as RefineDocTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain

# Sample test inputs
test_project_profile = {
    "title": "AI Ethics Policy",
    "scope_summary": "Create a federal guideline on ethical AI use",
    "strategic_alignment": "Supports digital innovation mandate",
    "key_stakeholders": "Treasury Board, ISED",
    "project_type": "Policy Development",
    "project_id": "proj-test-123"
}

test_memory = [
    {"input_summary": "Summary of past AI policy", "full_input_path": "/mem/ai_policy_2021.txt"},
    {"text": "AI ethics requires transparency and fairness."}
]

# Section test
print("\n[TEST] query_prompt_generator")
query_tool = QueryPromptTool()
query_output = query_tool.run_tool({"project_profile": test_project_profile, "memory": test_memory})
print("Query Output:", query_output)

print("\n[TEST] section_synthesizer")
synth_tool = SynthTool()
synth_output = synth_tool.run_tool({
    "artifact": "AI Ethics",
    "section": "Transparency",
    "project_profile": test_project_profile,
    "memory": test_memory,
    "corpus_answer": {"answer": "Transparency is a core principle."},
    "alignment_results": [],
    "web_search": "AI transparency efforts are underway globally."
})
print("Synth Output:", synth_output)

print("\n[TEST] section_refiner")
refine_tool = RefineTool()
refine_output = refine_tool.run_tool({"raw_draft": synth_output["raw_draft"]})
print("Refined Output:", refine_output)

print("\n[TEST] refine_document_chain")
refine_doc_tool = RefineDocTool()
refined_doc = refine_doc_tool.run_tool({"document_body": synth_output["raw_draft"]})
print("Refined Document:", refined_doc)

print("\n[TEST] generate_section_chain")
gen_chain = GenerateSectionChain()
chain_output = gen_chain.run({
    "artifact": "AI Ethics",
    "section": "Transparency",
    "project_profile": test_project_profile,
    "context_summary": "Focus on risks of unexplainable models.",
    "user_id": "user-test-1",
    "session_id": "sess-test-1"
})
print("Section Chain Output:", chain_output)

print("\n[TEST] assemble_artifact_chain")
assemble_chain = AssembleArtifactChain()
assemble_output = assemble_chain.run({
    "artifact": "AI Ethics",
    "gate_id": "0",
    "project_profile": test_project_profile,
    "user_id": "user-test-1",
    "session_id": "sess-test-1"
})
print("Assemble Output:", assemble_output)
