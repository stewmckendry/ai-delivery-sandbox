import os
import sys
import json
from dotenv import load_dotenv

# Set path to project root so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.engines.planner_orchestrator import PlannerOrchestrator

load_dotenv()

def run_test(intent, inputs):
    planner = PlannerOrchestrator()
    print(f"\n▶ Running intent: {intent}\nInputs: {json.dumps(inputs, indent=2)}")
    result = planner.run(intent, inputs)
    print("\n✅ Output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_test("external_web_search", {
        "query": "digital ID infrastructure",
        "search_type": "general"
    })

    run_test("external_web_search", {
        "query": "digital ID",
        "search_type": "jurisdiction",
        "context": {"location": "Canada"}
    })

    run_test("external_web_search", {
        "query": "identity verification",
        "search_type": "market",
        "context": {"industry": "financial services"}
    })

    run_test("generate_section", {
        "artifact": "test_artifact_001",
        "section": "security",
        "gate_id": "G1",
        "project_id": "TEST_PROJECT",
        "session_id": "s1",
        "user_id": "u1"
    })