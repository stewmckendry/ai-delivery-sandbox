import os
import sys
import json
from datetime import datetime

def default_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

# Add project root to sys.path so imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.engines.toolchains.IngestInputChain import IngestInputChain
from app.engines.toolchains.generate_section_chain import GenerateSectionChain
from app.engines.planner_orchestrator import PlannerOrchestrator

# Test Step 1: Ingest input and generate project profile
print("\n== Test 1: IngestInputChain ==")
ingest_input = {
    "input_method": "file",
    "file_path": "test_upload.txt",
    "metadata": {
        "artifact_id": "investment_proposal_concept",
        "gate_id": 0,
        "user_id": "test_user",
        "session_id": "s1",
        "project_id": "pegasus"
    }
}
ingest_output = IngestInputChain().run(ingest_input)
print(json.dumps(ingest_output, indent=2, default=default_serializer))
project_id = ingest_output.get("project_id")

# Test Step 2: Generate section using that project_id
print("\n== Test 2: GenerateSectionChain ==")
generate_input = {
    "artifact": "investment_proposal_concept",
    "section": "problem_statement",
    "gate_id": "0",
    "user_id": "test_user",
    "session_id": "s2",
    "project_id": project_id
}
generate_output = GenerateSectionChain().run(generate_input)
print(json.dumps(generate_output["save_result"], indent=2, default=default_serializer))

# Test Step 3: Assemble artifact via PlannerOrchestrator to inject project_profile
print("\n== Test 3: AssembleArtifactChain ==")
assemble_input = {
    "artifact_id": "investment_proposal_concept",
    "gate_id": "0",
    "version": "v1",
    "project_id": project_id
}
assemble_output = PlannerOrchestrator().run("assemble_artifact", assemble_input)
print(json.dumps(assemble_output, indent=2, default=default_serializer))