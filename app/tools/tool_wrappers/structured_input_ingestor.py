import yaml
import uuid
import datetime

def structure_input(raw_text, source, tool_name):
    return {
        'id': str(uuid.uuid4()),
        'source': source,
        'type': tool_name,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': raw_text,
        'content_summary': raw_text[:1000],
        'tags': ['input', 'upload']
    }

def to_yaml(entry_dict):
    return yaml.dump([entry_dict], sort_keys=False)

if __name__ == "__main__":
    example = structure_input("Sample content text here...", "user_upload.txt", "uploadTextInput")
    print(to_yaml(example))