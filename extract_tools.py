import yaml

with open("project/reference/tool_catalog.yaml") as f:
    data = yaml.safe_load(f)

with open("tool_list.txt", "w") as out:
    for key, val in data["tools"].items():
        module = val.get("module", "")
        description = val.get("description", "")
        out.write(f"  {key}:\n")
        out.write(f"    module: {module}\n")
        out.write(f"    description: {description}\n\n")