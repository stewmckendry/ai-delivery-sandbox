def build_fhir_bundle(symptoms, stage, incident, assessment, activity):
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }

    for s in symptoms:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "code": {"text": s.symptom_id},
                "valueInteger": s.score,
                "effectiveDateTime": s.timestamp.isoformat(),
                "note": [{"text": s.notes}] if s.notes else []
            }
        })

    if stage:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "code": {"text": "Recovery Stage"},
                "valueString": stage.name,
                "note": [{
                    "text": ", ".join(stage.allowed_activities + stage.progression_criteria)
                }]
            }
        })

    if assessment:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "code": {"text": "Concussion Assessment"},
                "valueString": "Concussion suspected" if assessment.inferred else "Low likelihood",
                "note": [{
                    "text": f"Red flags: {assessment.red_flags}; Moderate symptoms: {assessment.moderate_symptoms}"
                }]
            }
        })

    if activity:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "code": {"text": "Activity Check-In"},
                "valueString": activity.stage_attempted,
                "effectiveDateTime": activity.timestamp.isoformat(),
                "note": [{
                    "text": "Symptoms worsened" if activity.symptoms_worsened else "No symptom worsening"
                }]
            }
        })

    if incident:
        bundle["entry"].append({
            "resource": {
                "resourceType": "Observation",
                "code": {"text": "Incident Report"},
                "valueString": incident.injury_context,
                "effectiveDateTime": incident.injury_date.isoformat(),
                "note": [{"text": f"Sport: {incident.sport_type}, Age: {incident.age_group}"}]
            }
        })

    return bundle