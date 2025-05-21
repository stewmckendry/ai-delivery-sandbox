import yaml
import json
import argparse
from pathlib import Path
from urllib.request import urlopen

def load_gate_reference(source):
    if source.startswith("http"):
        with urlopen(source) as f:
            return yaml.safe_load(f.read())
    else:
        with open(source, 'r') as f:
            return yaml.safe_load(f)

def generate_scaffold(gate_list, gate_id, artifact_id):
    for gate in gate_list:
        if gate.get("gate_id") == gate_id:
            try:
                sections = gate['artifacts'][artifact_id]['sections']
            except KeyError:
                raise ValueError(f"Artifact ID '{artifact_id}' not found in gate '{gate_id}'.")

            scaffold = []
            for sec in sections:
                scaffold.append({
                    "section_id": sec.get('id'),
                    "title": sec.get('title'),
                    "content": "TODO: expand section",
                    "next_pod_hint": sec.get('owner', 'ExpanderPod')
                })

            return {
                "gate_id": gate_id,
                "artifact_id": artifact_id,
                "scaffold": scaffold
            }

    raise ValueError(f"Gate ID '{gate_id}' not found in gate reference list.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold gate document structure")
    parser.add_argument('--gate_id', required=True, help="Gate identifier (integer)")
    parser.add_argument('--artifact_id', required=True, help="Artifact identifier (e.g. 'business_case')")
    parser.add_argument('--ref_path', default="https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/gate_reference_v2.yaml", help="Path or URL to gate reference YAML")
    parser.add_argument('--output', default=None, help="Optional path to write scaffold JSON")
    args = parser.parse_args()

    gate_id = int(args.gate_id)  # Cast to integer since gate IDs are numbers
    gate_spec = load_gate_reference(args.ref_path)
    scaffold = generate_scaffold(gate_spec, gate_id, args.artifact_id)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(scaffold, f, indent=2)
    else:
        print(json.dumps(scaffold, f, indent=2))

if __name__ == "__main__":
    main()