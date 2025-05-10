from datetime import datetime

def build_fhir_bundle(tracker, symptom_logs):
    """
    Returns a FHIR Bundle containing:
    - Condition (Concussion)
    - One Observation per symptom log
    - CarePlan for recovery stage
    """
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }

    # ----- CONDITION -----
    # Represents the diagnosis of concussion
    # SNOMED code 71904000 is the standard code for "Concussion" per HL7 guidance
    condition = {
        "resourceType": "Condition",
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active"
            }]
        },
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "71904000",
                "display": "Concussion"
            }]
        },
        "subject": {"reference": f"Patient/{tracker['user_id']}"},
        "recordedDate": datetime.now().date().isoformat()
    }
    bundle["entry"].append({"resource": condition})

    # ----- OBSERVATIONS -----
    # Each symptom log becomes an Observation resource
    timestamps = []
    for log in symptom_logs:
        obs = {
            "resourceType": "Observation",
            "code": {"text": log["symptom_id"]},  # symptom name or ID
            "valueInteger": log["severity"],
            "subject": {"reference": f"Patient/{tracker['user_id']}"},
            "effectiveDateTime": log["timestamp"]  # ISO timestamp
        }
        timestamps.append(log["timestamp"])
        bundle["entry"].append({"resource": obs})

    # Infer CarePlan period from symptom timestamps
    if timestamps:
        period_start = min(timestamps)
        period_end = max(timestamps)
    else:
        today = datetime.now().date().isoformat()
        period_start = period_end = today

    # ----- CARE PLAN -----
    # Encodes recovery advice based on inferred stage
    care_plan = {
        "resourceType": "CarePlan",
        "status": "active",
        "intent": "plan",
        "title": "Concussion Recovery Plan",
        "description": "Rest, reduce screen time, and follow stage guidance",
        "subject": {"reference": f"Patient/{tracker['user_id']}"},
        "period": {
            "start": period_start,
            "end": period_end
        }
    }
    bundle["entry"].append({"resource": care_plan})

    return bundle