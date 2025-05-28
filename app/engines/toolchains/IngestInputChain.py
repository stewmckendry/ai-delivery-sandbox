from app.tools.tool_registry import load_tool

class IngestInputChain:
    def run(self, inputs):
        tool_type = inputs.get("upload_type")
        upload_tool = load_tool(tool_type)

        # Don't save profile if inside chain
        upload_result = upload_tool.run_tool(inputs, log_usage=False, save_profile=False)
        return upload_result