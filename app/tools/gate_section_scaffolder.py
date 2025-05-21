import yaml
import json
import argparse
from pathlib import Path

def load_gate_reference(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def generate_scaffold(gate_spec, gate_id):
    if gate_id not in gate_spec:
        raise ValueError(f"Gate ID '{gate_id}' not found in gate reference.")

    sections = gate_spec[gate_id]['sections']
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
        "scaffold": scaffold
    }

def main():
    parser = argparse.ArgumentParser(description="Scaffold gate document structure")
    parser.add_argument('--gate_id', required=True, help="Gate identifier")
    parser.add_argument('--ref_path', default="project/reference/gate_reference_v2.yaml", help="Path to gate reference YAML")
    parser.add_argument('--output', default=None, help="Optional path to write scaffold JSON")
    args = parser.parse_args()

    gate_spec = load_gate_reference(args.ref_path)
    scaffold = generate_scaffold(gate_spec, args.gate_id)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(scaffold, f, indent=2)
    else:
        print(json.dumps(scaffold, indent=2))

if __name__ == "__main__":
    main()