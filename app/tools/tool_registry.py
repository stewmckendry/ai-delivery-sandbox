import importlib
import yaml
import os
import requests
from jsonschema import validate, ValidationError
import app.tools.tool_wrappers.loadCorpus
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("📦 Registry loaded")

    def get_tool(self, tool_id):
        logger.info(f"📦 Loading tool: {tool_id}")
        tool_entry = self.catalog.get(tool_id)
        if not tool_entry:
            raise ValueError(f"Tool '{tool_id}' not found")

        module_path = tool_entry["module"]
        class_name = tool_entry.get("class", "Tool")
        logger.info(f"📦 Importing {module_path}.{class_name}")
        module = importlib.import_module(module_path)
        logger.info(f"📦 Imported {module_path}.{class_name}")
        tool_class = getattr(module, class_name)
        tool_instance = tool_class()
        logger.info("📦 Checking schema")
        if "schema" in tool_entry:
            setattr(tool_instance, "schema", tool_entry["schema"])
            setattr(tool_instance, "validate", lambda input_dict: self._validate(input_dict, tool_entry["schema"]))
        logger.info("📦 Tool loaded")
        return tool_instance

    def list_tools(self):
        return [
            {"tool_id": tool_id, **entry}
            for tool_id, entry in self.catalog.items()
        ]

    def _validate(self, input_dict, schema):
        try:
            logger.info(f"Validating input: {input_dict} against schema: {schema}")
            validate(instance=input_dict, schema=schema)
            logger.info("Validation successful")
        except ValidationError as e:
            logger.error(f"Validation error: {e.message}")
            raise ValueError(f"Input validation error: {e.message}")