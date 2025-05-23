from app.db.models.PromptLog import PromptLog
from app.db.database import get_session
from datetime import datetime

class Tool:
    def validate(self, input_dict):
        if "artifact" not in input_dict or "section" not in input_dict:
            raise ValueError("artifact and section are required")

    def run_tool(self, input_dict):
        self.validate(input_dict)
        artifact = input_dict["artifact"]
        section = input_dict["section"]
        session_id = input_dict.get("session_id")
        user_id = input_dict.get("user_id")

        tool_names = ["uploadTextInput", "uploadFileInput", "uploadLinkInput"]

        session = get_session()
        query = session.query(PromptLog).filter(
            PromptLog.tool.in_(tool_names),
            PromptLog.full_input_path.like(f'%"artifact": "{artifact}"%'),
            PromptLog.full_input_path.like(f'%"section": "{section}"%')
        )
        if session_id:
            query = query.filter(PromptLog.session_id == session_id)
        if user_id:
            query = query.filter(PromptLog.user_id == user_id)

        entries = query.order_by(PromptLog.timestamp.asc()).all()

        return [{
            "input_summary": e.input_summary,
            "output_summary": e.output_summary,
            "full_input_path": e.full_input_path,
            "timestamp": e.timestamp.isoformat()
        } for e in entries]