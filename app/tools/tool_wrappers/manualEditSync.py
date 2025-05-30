import logging
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection

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
        session_id = input_dict.get("session_id")

        # Fetch current section text
        db = get_session()
        section_record = db.query(ArtifactSection).filter_by(artifact_id=artifact_id, section_id=section_id, project_id=project_id, session_id=session_id).order_by(ArtifactSection.timestamp.desc()).first()
        current_text = section_record.text if section_record else ""

        if revised_text.strip() == current_text.strip():
            log_tool_usage("manualEditSync", "no change", revised_text, session_id, user_id, input_dict)
            return {"status": "no_change", "section_id": section_id}

        trace = []
        output = {"input": input_dict, "output": revised_text, "tool": "manualEditSync", "note": "User manually edited the section text."}  
        trace.append({"tool": "section_refiner", "output": output})

        result = save_artifact_and_trace(
            section_id=section_id,
            artifact_id=artifact_id,
            gate_id=gate_id,
            text=revised_text,
            sources="manual user input",
            tool_outputs=trace,
            user_id=user_id,
            project_id=project_id
        )

        logger.info(f"Manual edit saved for section {section_id}")
        return {"status": "saved", "section_id": section_id, "trace_id": result["trace_id"]}