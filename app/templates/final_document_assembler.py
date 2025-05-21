import json
import argparse
from pathlib import Path
from datetime import datetime

def assemble(expanded_path, doc_id):
    with open(expanded_path, 'r') as f:
        data = json.load(f)

    lines = [f"# Gate Document: {doc_id}", f"Generated: {datetime.utcnow().isoformat()} UTC", ""]
    gateblock = {
        "doc_id": doc_id,
        "gate_id": data["gate_id"],
        "artifact_id": data["artifact_id"],
        "session_id": data["session_id"],
        "sections": []
    }

    for section in data["expanded_sections"]:
        lines.append(f"## {section['title']}")
        lines.append(section['content'])
        lines.append("")

        gateblock["sections"].append({
            "section_id": section["section_id"],
            "title": section["title"],
            "content": section["content"]
        })

    out_dir = Path("docs/working")
    out_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{doc_id}.md"
    json_path = out_dir / f"{doc_id}_gateblock.json"

    with open(md_path, 'w') as f:
        f.write("\n".join(lines))

    with open(json_path, 'w') as f:
        json.dump(gateblock, f, indent=2)

    print(f"✅ Markdown written to: {md_path}")
    print(f"✅ Gateblock JSON written to: {json_path}")

def main():
    parser = argparse.ArgumentParser(description="Assemble expanded sections into gate document")
    parser.add_argument('--expanded_path', required=True, help="Path to expanded JSON")
    parser.add_argument('--doc_id', required=True, help="Document ID for output")
    args = parser.parse_args()

    assemble(args.expanded_path, args.doc_id)

if __name__ == "__main__":
    main()