import json
import argparse
from pathlib import Path

def expand_section(section, session_id):
    return {
        "section_id": section.get("section_id"),
        "title": section.get("title"),
        "content": f"[GPT: Expanded section using session '{session_id}']",
        "next_pod_hint": section.get("next_pod_hint")
    }

def main():
    parser = argparse.ArgumentParser(description="Expand scaffolded sections via GPT + memory")
    parser.add_argument('--scaffold_path', required=True, help="Path to scaffold JSON")
    parser.add_argument('--session_id', required=True, help="Session memory ID")
    parser.add_argument('--output', required=True, help="Path to write expanded JSON")
    args = parser.parse_args()

    with open(args.scaffold_path, 'r') as f:
        scaffold = json.load(f)

    expanded = {
        "gate_id": scaffold["gate_id"],
        "artifact_id": scaffold["artifact_id"],
        "session_id": args.session_id,
        "sections": [expand_section(sec, args.session_id) for sec in scaffold["scaffold"]]
    }

    with open(args.output, 'w') as f:
        json.dump(expanded, f, indent=2)

if __name__ == "__main__":
    main()