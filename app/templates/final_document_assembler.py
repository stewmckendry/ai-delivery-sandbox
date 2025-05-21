import json
import argparse

def assemble_document(expanded_doc, doc_id):
    sections = expanded_doc.get("sections", [])
    content_md = f"# Document: {doc_id}\n\n"
    content_json = {
        "doc_id": doc_id,
        "gate_id": expanded_doc.get("gate_id"),
        "artifact_id": expanded_doc.get("artifact_id"),
        "session_id": expanded_doc.get("session_id"),
        "sections": []
    }

    for sec in sections:
        content_md += f"## {sec.get('title')}\n\n{sec.get('content')}\n\n"
        content_json["sections"].append({
            "section_id": sec.get("section_id"),
            "title": sec.get("title"),
            "content": sec.get("content")
        })

    return content_md, content_json

def main():
    parser = argparse.ArgumentParser(description="Assemble expanded sections into gate document")
    parser.add_argument('--expanded_path', required=True, help="Path to expanded JSON")
    parser.add_argument('--doc_id', required=True, help="Document ID for output")
    parser.add_argument('--output_md', help="Optional path to write Markdown output")
    parser.add_argument('--output_json', help="Optional path to write JSON output")
    args = parser.parse_args()

    with open(args.expanded_path, 'r') as f:
        expanded_doc = json.load(f)

    md, js = assemble_document(expanded_doc, args.doc_id)

    if args.output_md:
        with open(args.output_md, 'w') as f:
            f.write(md)
    else:
        print("--- Markdown Output ---\n")
        print(md)

    if args.output_json:
        with open(args.output_json, 'w') as f:
            json.dump(js, f, indent=2)
    else:
        print("--- JSON Output ---\n")
        print(json.dumps(js, indent=2))

if __name__ == "__main__":
    main()