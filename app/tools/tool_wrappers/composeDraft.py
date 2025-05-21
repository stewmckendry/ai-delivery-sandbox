class Tool:
    def run_tool(self, input_dict):
        self.validate(input_dict)
        return {"status": "not_implemented", "tool": "composeDraft"}