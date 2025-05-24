from app.engines.planner_orchestrator import PlannerOrchestrator

def run_successful_test():
    print("\nRunning successful assemble_artifact test")
    result = PlannerOrchestrator().run("assemble_artifact", {
        "artifact_id": "investment_proposal_concept",
        "gate_id": "0",
        "version": "v0.1"
    })
    print("SUCCESSFUL TEST RESULT:\n", result)


def run_invalid_artifact_test():
    print("\nRunning invalid artifact_id test")
    try:
        result = PlannerOrchestrator().run("assemble_artifact", {
            "artifact_id": "nonexistent_artifact",
            "gate_id": "0"
        })
        print("UNEXPECTED SUCCESS:\n", result)
    except Exception as e:
        print("EXPECTED ERROR:\n", e)


if __name__ == "__main__":
    run_successful_test()
    run_invalid_artifact_test()