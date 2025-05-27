import os
import pprint
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.toolchains.assemble_artifact_chain import AssembleArtifactChain
from app.engines.toolchains.generate_full_artifact_chain import GenerateFullArtifactChain

pp = pprint.PrettyPrinter(indent=2)

def run_toolchain(name, chain_cls, input_data):
    print(f"\n=== Running {name} ===")
    chain = chain_cls()
    result = chain.run(input_data)
    print("Result:")
    pp.pprint(result)
    print(f"=== Finished {name} ===\n")
    return result

if __name__ == "__main__":
    project_id = "test_project"
    artifact_id = "test_artifact"
    section_id = "test_section"
    user_id = "test_user"

    # Generate Section Chain Test
    section_input = {
        "artifact": artifact_id,
        "section": section_id,
        "project_profile": {
            "project_id": project_id,
            "title": "Test Project",
            "scope_summary": "This is a scope summary.",
            "strategic_alignment": "Supports climate goals.",
            "key_stakeholders": "Internal team, clients",
            "project_type": "Policy"
        },
        "session_id": "test_session",
        "user_id": user_id,
        "gate_id": "0"
    }
    run_toolchain("generate_section_chain", GenerateSectionChain, section_input)

    # Assemble Artifact Chain Test
    assemble_input = {
        "artifact": artifact_id,
        "user_id": user_id,
        "project_id": project_id
    }
    run_toolchain("assemble_artifact_chain", AssembleArtifactChain, assemble_input)

    # Full Artifact Generation Chain Test
    full_artifact_input = {
        "project_id": project_id,
        "artifact": artifact_id,
        "user_id": user_id,
        "gate_id": "0",
        "session_id": "test_session"
    }
    run_toolchain("generate_full_artifact_chain", GenerateFullArtifactChain, full_artifact_input)