import argparse
from app.tools.tool_wrappers.uploadTextInput import Tool as UploadTool
from app.tools.tool_wrappers.inputChecker import Tool as InputCheckerTool
from app.tools.tool_wrappers.confirmProjectProfile import Tool as ProjectProfileTool
from app.engines.toolchains.generate_section_chain import GenerateSectionChain


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
    print("Missing Intents:", checker_result)

    print("[3] Loading project profile...")
    profile_result = ProjectProfileTool().run_tool({"project_id": project_id})
    print("Project Name:", profile_result["project_profile"].get("name"))

    print("[4] Generating section draft...")
    chain = GenerateSectionChain()
    section_result = chain.run({
        "session_id": session_id,
        "user_id": user_id,
        "gate_id": gate_id,
        "artifact": artifact,
        "section": section,
        "project_id": project_id,
        "project_profile": profile_result["project_profile"]
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