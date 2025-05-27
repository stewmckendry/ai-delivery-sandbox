import logging
from app.engines.memory_sync import save_artifact_and_trace

logger = logging.getLogger(__name__)

class Tool:
    def validate(self, input_dict):
        required = ["section", "artifact", "user_id", "project_id", "feedback_text"]
        for field in required:
            if field not in input_dict:
                raise ValueError(f"Missing required input: {field}")

    def run_tool(self, input_dict):
        self.validate(input_dict)

        section_id = input_dict["section"]
        artifact_id = input_dict["artifact"]
        user_id = input_dict["user_id"]
        project_id = input_dict["project_id"]
        revised_text = input_dict["feedback_text"]
        gate_id = input_dict.get("gate_id", "0")

        log = {
            "tool": "manualEditSync",
            "input": input_dict,
            "output": revised_text,
            "note": "Manual override saved directly."
        }

        result = save_artifact_and_trace(
            section_id=section_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            text=revised_text,
            sources="manual user input",
            tool_outputs=[log],
            user_id=user_id,
            project_id=project_id
        )

        logger.info(f"Manual edit saved for section {section_id}")
        return {"status": "saved", "section_id": section_id, "trace_id": result["trace_id"]}