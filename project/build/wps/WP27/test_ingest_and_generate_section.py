import argparse
import sys
import os

# Ensure the project root is in sys.path so imports like app.tools... work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print("sys.path:", sys.path)
print("project_root:", project_root)

from app.tools.tool_wrappers.uploadTextInput import Tool as UploadTool
from app.tools.tool_wrappers.inputChecker import Tool as InputCheckerTool
# from app.tools.tool_wrappers.confirmProjectProfile import Tool as ProjectProfileTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain

"""
Script: test_ingest_and_generate_section.py
Purpose: Validates the end-to-end flow for uploading user input, validating metadata, and generating a draft
         for a selected section of a policy artifact. ProjectProfile step skipped for now.

Test Flow:
1. Upload sample input text for a given section.
2. Validate that all required inputs and intents are present.
3. Generate a draft section using the configured toolchain (with a stub profile).

Usage:
python project/build/wps/WP27/test_ingest_and_generate_section.py \
  --project_id "test_project_id_iteration2" \
  --session_id "test_session_id_iteration2" \
  --user_id "test_user_id_iteration2" \
  --text_file project/build/wps/WP27/sample_input_text.txt

Defaults:
  gate_id = 0
  artifact = investment_proposal_concept
  section = problem_context
"""

def main(project_id, session_id, user_id, gate_id, artifact, section, text_file):
    with open(text_file, 'r') as file:
        raw_text = file.read()

    print("[1] Uploading input text...")
    upload_result = UploadTool().run_tool({
        "text": raw_text,
        "metadata": {
            "project_id": project_id,
            "artifact_id": artifact,
            "gate_id": gate_id,
            "section_id": section,
            "session_id": session_id,
            "user_id": user_id,
            "intent": "problem_context"
        }
    })
    print("Uploaded:", upload_result["status"])

    print("[2] Validating input intents...")
    checker_result = InputCheckerTool().run_tool({
        "session_id": session_id,
        "gate_id": int(gate_id),
        "artifact_id": artifact
    })
    print("Intent Coverage Report:")
    print("  ✅ Covered:")
    for section_id, intents in checker_result.get("covered", {}).items():
        print(f"    [{section_id}]: {', '.join(intents)}")
    print("  ❌ Missing:")
    for section_id, intents in checker_result.get("missing", {}).items():
        print(f"    [{section_id}]: {', '.join(intents)}")

    print("[3] Generating section draft (stub profile)...")
    stub_profile = {
        "name": "Digital Identity Modernization",
        "description": "Unifying digital identity efforts across departments.",
        "program_context": "Cross-government initiative targeting trust and usability."
    }

    chain = GenerateSectionChain()
    section_result = chain.run({
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact": artifact,
        "section": section,
        "project_id": project_id,
        "project_profile": stub_profile
    })
    print("\n=== Draft Output ===")
    print(section_result["final_output"]["raw_draft"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test ingestion and section generation flow")
    parser.add_argument('--project_id', required=True)
    parser.add_argument('--session_id', required=True)
    parser.add_argument('--user_id', required=True)
    parser.add_argument('--gate_id', default="0")
    parser.add_argument('--artifact', default="investment_proposal_concept")
    parser.add_argument('--section', default="problem_context")
    parser.add_argument('--text_file', required=True)

    args = parser.parse_args()
    main(args.project_id, args.session_id, args.user_id, args.gate_id, args.artifact, args.section, args.text_file)