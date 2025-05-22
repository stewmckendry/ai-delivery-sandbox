import importlib
import yaml
import os
import requests
from jsonschema import validate, ValidationError

class ToolRegistry:
    def __init__(self, source="local"):
        self.source = source
        if source == "github":
            url = "https://raw.githubusercontent.com/stewmckendry/ai-delivery-sandbox/sandbox-curious-falcon/project/reference/tool_catalog.yaml"
            r = requests.get(url)
            self.catalog = yaml.safe_load(r.text)["tools"]
        else:
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
        try:
            print(f"Validating input against schema: {schema}")
            validate(instance=input_dict, schema=schema)
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            raise ValueError(f"Input validation error: {e.message}")