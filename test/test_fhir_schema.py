from app.engines.epic_writer import build_fhir_bundle

def test_fhir_bundle_structure():
    tracker = {'user_id': 'test-user', 'state': {'stage': 'Stage 1'}}
    logs = [
        {'symptom_id': 'dizziness', 'severity': 2, 'timestamp': '2025-05-01T08:00:00Z'},
        {'symptom_id': 'fatigue', 'severity': 3, 'timestamp': '2025-05-01T09:00:00Z'}
    ]

    bundle = build_fhir_bundle(tracker, logs)

    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert isinstance(bundle["entry"], list)

    resources = [e["resource"] for e in bundle["entry"]]
    types = set(r["resourceType"] for r in resources)

    assert "Condition" in types
    assert "Observation" in types
    assert "CarePlan" in types

    condition = next(r for r in resources if r["resourceType"] == "Condition")
    assert condition["code"]["coding"][0]["code"] == "71904000"

    care_plan = next(r for r in resources if r["resourceType"] == "CarePlan")
    assert "period" in care_plan