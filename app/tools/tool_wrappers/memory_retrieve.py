from app.db.models.PromptLog import PromptLog
from app.db.database import get_session
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class Tool:
    def run_tool(self, input_dict):
        logger.info("[Tool] memory_retrieve started")
        artifact = input_dict["artifact"]
        session_id = input_dict.get("session_id")
        user_id = input_dict.get("user_id")
        project_id = input_dict.get("project_id")

        tool_names = ["uploadTextInput", "uploadFileInput", "uploadLinkInput"]

        session = get_session()
        logger.info(f"Retrieving entries for artifact={artifact}, project_id={project_id}")
        query = session.query(PromptLog).filter(
            PromptLog.tool.in_(tool_names),
            PromptLog.full_input_path.contains(f'"artifact_id": "{artifact}"'),
            PromptLog.project_id == project_id
        )
        if session_id:
            query = query.filter(PromptLog.session_id == session_id)

        # commented out PromptLog.full_input_path.contains(f'"section_id": "{section}"') from query as inputs are global; tailoring is based on section intents    

        entries = query.order_by(PromptLog.timestamp.asc()).all()
        # Remove entries with duplicate output_summary, keeping the first occurrence
        seen_summaries = set()
        unique_entries = []
        for entry in entries:
            if entry.output_summary not in seen_summaries:
                unique_entries.append(entry)
                seen_summaries.add(entry.output_summary)
        entries = unique_entries
        logger.info(f"Found {len(entries)} entries for artifact={artifact}, section={section}, session_id={session_id}, user_id={user_id}")
        return [{
            "input_summary": e.input_summary,
            "output_summary": e.output_summary,
            "full_input_path": e.full_input_path,
            "timestamp": e.timestamp.isoformat()
        } for e in entries]