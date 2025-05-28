class Tool:
    def run_tool(self, input_dict):
        self.validate(input_dict)
        return {
            "status": "not_implemented",
            "tool": "translateDocument"
        }

    def validate(self, input_dict):
        required = ["doc_id", "target_lang"]
        for field in required:
            if field not in input_dict:
                raise ValueError(f"Missing required field: {field}")

        if input_dict["target_lang"] not in ["en", "fr"]:
            raise ValueError("Invalid value for target_lang: must be 'en' or 'fr'")