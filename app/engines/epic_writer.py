from datetime import datetime

def build_fhir_bundle(symptoms: list, stage: str, incident: object = None):
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }

    for entry in symptoms:
        obs = {
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {"text": entry["symptom_id"]},
                "valueInteger": entry.get("severity"),
                "effectiveDateTime": entry.get("timestamp"),
                "extension": [
                    {"url": "reporter", "valueString": entry.get("reporter_type")},
                    {"url": "incident_context", "valueString": entry.get("incident_context")},
                    {"url": "sport_type", "valueString": entry.get("sport_type")},
                    {"url": "age_group", "valueString": entry.get("age_group")},
                    {"url": "team_id", "valueString": entry.get("team_id")},
                ]
            }
        }
        bundle["entry"].append(obs)

    if stage:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "status": "final",
                "code": {"text": "Inferred Recovery Stage"},
                "valueString": stage,
                "effectiveDateTime": datetime.utcnow().isoformat()
            }
        })

    return bundle