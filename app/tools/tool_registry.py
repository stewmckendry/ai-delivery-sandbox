import importlib
import yaml
import os

class ToolRegistry:
    def __init__(self):
        catalog_path = os.path.join("project", "reference", "tool_catalog.yaml")
        with open(catalog_path, "r") as f:
            self.catalog = yaml.safe_load(f)["tools"]

    def get_tool(self, tool_id):
        tool_entry = self.catalog.get(tool_id)
        if not tool_entry:
            raise ValueError(f"Tool '{tool_id}' not found")

        module_path = tool_entry["module"]
        class_name = tool_entry.get("class", "Tool")

        module = importlib.import_module(module_path)
        tool_class = getattr(module, class_name)
        tool_instance = tool_class()

        if "schema" in tool_entry:
            setattr(tool_instance, "schema", tool_entry["schema"])
            setattr(tool_instance, "validate", lambda input_dict: self._validate(input_dict, tool_entry["schema"]))

        return tool_instance

    def list_tools(self):
        return [
            {"tool_id": tool_id, **entry}
            for tool_id, entry in self.catalog.items()
        ]

    def _validate(self, input_dict, schema):
        missing = [k for k in schema if k not in input_dict]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        for key, rule in schema.items():
            if "enum" in rule:
                if input_dict.get(key) not in rule["enum"]:
                    raise ValueError(f"Invalid value for {key}: must be one of {rule['enum']}")