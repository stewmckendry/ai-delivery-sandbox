import sys
import os

# Set path to project root so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.engines.planner_orchestrator import PlannerOrchestrator

if __name__ == "__main__":
    planner = PlannerOrchestrator()
    output = planner.run(
        intent="generate_section",
        inputs={
            "artifact": "investment_proposal_concept",
            "section": "problem_statement",
            "session_id": "test-session-001",
            "user_id": "test-user-001"
        }
    )

    print("✅ Final Output:\n")
    print(output["final_output"]["refined_draft"])

    print("\n📜 Trace:\n")
    for step in output["trace"]:
        print(f"{step['tool']}: {list(step['output'].keys())}")