import logging
from app.redis.redis_client import redis_client
from app.tools.tool_registry import ToolRegistry
import json
import datetime

logger = logging.getLogger(__name__)

class Tool:

    def run_tool(self, input_dict):
        section_id = input_dict["section_id"]
        feedback_text = input_dict["feedback"]
        revision_type = input_dict.get("revision_type", "rewrite")
        artifact_id = input_dict["artifact_id"]
        project_id = input_dict["project_id"]
        session_id = input_dict.get("session_id", "default")

        registry = ToolRegistry()
        rewriter = registry.get_tool("section_rewriter")
        diff_tool = registry.get_tool("diff_summarizer")
        memory_tool = registry.get_tool("memory_retrieve")

        # Construct Redis key
        redis_key = f"section_revision:{project_id}:{artifact_id}:{section_id}"
        raw_data = redis_client.get(redis_key)
        if not raw_data:
            return {"status": "error", "message": f"Section {section_id} not found in Redis"}
        
        parsed = json.loads(raw_data)
        original = parsed.get("text")
        logger.info(f"Original section text for {section_id}: {original[:100]}...")

        memory = memory_tool.run_tool({"artifact_id": artifact_id, "project_id": project_id, "session_id": session_id})

        revised = rewriter.run_tool({
            "section_id": section_id,
            "memory": memory,
            "feedback": feedback_text,
            "revision_type": revision_type,
            "current_text": original,
            **input_dict
        })

        diff = diff_tool.run_tool({"original": original, "revised": revised["draft"]})

        updated = {
            "text": revised["draft"],
            "diff_summary": diff["diff_summary"],
            "status": "updated",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        redis_client.set(redis_key, json.dumps(updated))

        return {
            "status": "updated",
            "section_id": section_id,
            "diff_summary": updated["diff_summary"],
            "instructions": (
                "Here is the revised section based on your feedback, along with a summary of what changed. "
                "You should now present the new draft and the diff to the user. Ask if they’d like to revise it again "
                "(if yes, call `section_review_feedback` again), or if it’s ready to move to the next section. "
                "Once approved, proceed to call `generateSectionDraft` with the next `section_id` in the artifact."
            )
        }
