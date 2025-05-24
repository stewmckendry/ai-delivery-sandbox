import requests
import yaml
from typing import Optional

GATE_REF_URL = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml"

def generate_template_for_artifact(artifact_id: str) -> Optional[str]:
    """
    Dynamically generate a markdown template for an artifact using gate_reference_v2.yaml
    """
    response = requests.get(GATE_REF_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch gate reference file")

    gates = yaml.safe_load(response.text)

    for gate in gates:
        for artifact in gate.get("artifacts", []):
            if artifact.get("artifact_id") == artifact_id:
                template_lines = [f"# {artifact.get('name')}\n"]
                for section in artifact.get("sections", []):
                    section_title = section.get("title", section.get("section_id"))
                    template_lines.append(f"\n## {section_title}\n")
                    template_lines.append("\nTODO: Fill in this section.\n")
                return "\n".join(template_lines)
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python generate_artifact_template.py <artifact_id>")
        exit(1)
    artifact_id = sys.argv[1]
    output = generate_template_for_artifact(artifact_id)
    if output:
        print(output)
    else:
        print("Artifact not found.")