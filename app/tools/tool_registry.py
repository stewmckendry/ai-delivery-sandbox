import importlib
import yaml
from pathlib import Path

class ToolRegistry:
    def __init__(self, config_path="project/reference/tool_catalog.yaml"):
        self.config_path = Path(config_path)
        self.tools = {}
        self.load_tools()

    def load_tools(self):
        with self.config_path.open() as f:
            catalog = yaml.safe_load(f)
        for tool_id, entry in catalog.get("tools", {}).items():
            module_path = entry["module"]
            class_name = entry.get("class", "Tool")
            mod = importlib.import_module(module_path)
            tool_class = getattr(mod, class_name)
            self.tools[tool_id] = tool_class()

    def get_tool(self, tool_id):
        return self.tools.get(tool_id)

    def list_tools(self):
        return list(self.tools.keys())