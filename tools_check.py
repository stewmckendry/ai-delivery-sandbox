import os
import yaml
import json

# 1. Filenames in app/tools/tool_wrappers (no extension)
wrapper_files = set(
    f[:-3] for f in os.listdir('app/tools/tool_wrappers') if f.endswith('.py')
)

# 2. Keys under tools in tool_catalog.yaml
with open('project/reference/tool_catalog.yaml') as f:
    tools_yaml = yaml.safe_load(f)
yaml_keys = set(tools_yaml['tools'].keys())

# 3. tool_id in gpt_tools_manifest.json
with open('project/reference/gpt_tools_manifest.json') as f:
    tools_json = json.load(f)
json_ids = set(t['tool_id'] for t in tools_json['tools'])

print("In wrappers but not in YAML:", wrapper_files - yaml_keys)
print("In YAML but not in wrappers:", yaml_keys - wrapper_files)
print("In YAML but not in JSON:", yaml_keys - json_ids)
print("In JSON but not in YAML:", json_ids - yaml_keys)