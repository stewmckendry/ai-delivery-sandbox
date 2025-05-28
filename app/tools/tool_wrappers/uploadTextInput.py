from app.db.models.TextInput import TextInput
from app.db.database import db
from app.tools.tool_interfaces import ToolInterface
from app.models.input_models import TextInputModel
from app.utils.logger import logger
from app.utils.key_generator import generate_unique_id
from app.engines.project_profile_engine import ProjectProfileEngine

class Tool(ToolInterface):
    def run_tool(self, input_dict, log_usage=True):
        validated_input = TextInputModel(**input_dict)
        text = validated_input.text
        metadata = validated_input.metadata
        save_profile = input_dict.get("save_profile", False)

        new_input = TextInput(
            text=text,
            metadata=metadata,
            session_id=validated_input.session_id,
            user_id=validated_input.user_id,
            gate_id=validated_input.gate_id,
            project_id=validated_input.project_id,
            artifact=validated_input.artifact,
            section=validated_input.section,
            input_id=generate_unique_id()
        )
        db.add(new_input)
        db.commit()

        if save_profile:
            ProjectProfileEngine().generate_and_save(text, metadata)

        return {"status": "success", "input_id": new_input.input_id}