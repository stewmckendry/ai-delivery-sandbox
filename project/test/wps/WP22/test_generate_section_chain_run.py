import json
from app.engines.toolchains.generate_section_chain import GenerateSectionChain

inputs = {
    "artifact": "Digital Strategy",
    "section": "Open Government Policies",
    "project_profile": {
        "project_id": "P123",
        "title": "Open Government Data Initiative",
        "scope_summary": "Develop a federal policy to promote open data use",
        "strategic_alignment": "Supports Canada’s Digital Strategy and Data Governance",
        "key_stakeholders": "TBS, SSC, Statistics Canada",
        "project_type": "Policy"
    },
    "session_id": "test-session-001",
    "user_id": "dev-tester"
}

if __name__ == "__main__":
    chain = GenerateSectionChain()
    output = chain.run(inputs)
    print("\n=== Final Output ===")
    print(json.dumps(output["final_output"], indent=2))
    print("\n=== Trace ===")
    for step in output["trace"]:
        print(f"[Tool: {step['tool']}]\n{json.dumps(step['output'], indent=2)}\n")
    print("\n=== Save Result ===")
    print(json.dumps(output["save_result"], indent=2))