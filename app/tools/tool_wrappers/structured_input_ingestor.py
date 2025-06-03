import yaml
import uuid
import datetime

def structure_input(raw_text, source, tool_name, metadata=None):
    return {
        'id': str(uuid.uuid4()),
        'tool': tool_name,
        'input_summary': f"{source} | {tool_name}",
        'output_summary': raw_text[:1000],
        'full_input_path': None,
        'full_output_path': None,
        'session_id': metadata.get("session_id"),
        'user_id': metadata.get("user_id"),
        'project_id': metadata.get("project_id"),  # NEW: capture project
        'metadata': metadata or {},
        'timestamp': datetime.datetime.utcnow()
    }

def to_yaml(entry_dict):
    return yaml.dump([entry_dict], sort_keys=False)

if __name__ == "__main__":
    example = structure_input("Sample content text here...", "user_upload.txt", "uploadTextInput", metadata={"gate": 0, "artifact": "investment_proposal_concept"})
    print(to_yaml(example))