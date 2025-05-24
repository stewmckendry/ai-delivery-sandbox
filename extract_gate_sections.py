import yaml

with open("project/reference/gate_reference_v2.yaml") as f:
    gates = yaml.safe_load(f)

with open("gate_sections.txt", "w") as out:
    for gate in gates:
        out.write(f"- gate_id: {gate['gate_id']}\n")
        out.write(f"  name: {gate['name']}\n")
        for artifact in gate.get("artifacts", []):
            out.write(f"  - artifact_id: {artifact['artifact_id']}\n")
            out.write(f"    name: {artifact['name']}\n")
            for section in artifact.get("sections", []):
                out.write(f"    - section_id: {section['section_id']}\n")
                out.write(f"      title: {section['title']}\n")