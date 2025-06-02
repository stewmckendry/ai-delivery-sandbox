import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage, save_feedback
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection
from app.tools.utils.llm_helpers import chat_completion_request
from app.redis.redis_client import redis_client
import json
from jinja2 import Template
from app.tools.utils.llm_helpers import get_prompt

logger = logging.getLogger(__name__)

class ReviseSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.feedback_preprocessor = registry.get_tool("feedback_preprocessor")
        self.feedback_mapper = registry.get_tool("feedback_mapper")
        self.section_rewriter = registry.get_tool("section_rewriter")
        self.manual_edit_tool = registry.get_tool("manualEditSync")
        self.structurer = registry.get_tool("feedback_structurer")
        self.diff_summarizer = registry.get_tool("diff_summarizer")


    def summarize_text(self, text):
        if not text or len(text.split()) < 100:
            return text
        prompt = f"Summarize the following artifact section in one paragraph:\n\n{text}"
        return chat_completion_request(prompt)

    def run_tool(self, inputs):
        trace = []
        artifact_id = inputs.get("artifact_id")
        raw_feedback = inputs.get("feedback_text")
        mode = inputs.get("mode")
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        project_id = inputs.get("project_id")

        # Step 1: memory
        memory_input = {**inputs}
        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        # Summarize current artifact sections
        db = get_session()
        all_records = db.query(ArtifactSection).filter_by(
            artifact_id=artifact_id, project_id=project_id, session_id=session_id
        ).order_by(ArtifactSection.timestamp.desc()).all()
        latest_sections = {}
        for sec in all_records:
            if sec.section_id not in latest_sections:
                latest_sections[sec.section_id] = sec
        logger.info("[Step 2] Retrieved latest sections from ArtifactSection")

        summarized_sections = [
            {"section_id": sid, "text": self.summarize_text(sec.text)}
            for sid, sec in latest_sections.items()
        ]
        logger.info("[Step 2.5] Summarized latest sections")

        feedback_entries = inputs.get("feedback_entries")
        if feedback_entries:
            logger.info("[Step 3] Using direct feedback_entries from inputs")
            feedback_map = {}
            for entry in feedback_entries:
                sid = entry["section_id"]
                feedback_map.setdefault(sid, []).append(entry)
        else:
            structure_input = {
                "feedback_entries": raw_feedback,
                "sections": summarized_sections,
                **inputs
            }
            logger.info("[Step 3] Preparing to run feedback structurer with input")

            structured = self.structurer.run_tool(structure_input)
            trace.append({"tool": "feedback_structurer", "output": structured})
            logger.info("[Step 4] feedback_structurer complete")

            feedback_map = structured.get("section_feedback_map")

        if not isinstance(feedback_map, dict):
            logger.warning("Malformed or missing section_feedback_map. Skipping revisions.")
            return {
                "trace": trace,
                "status": "error",
                "message": "Invalid feedback structure. Expected section_feedback_map dictionary."
            }

        # Step 3: log original feedback
        save_feedback(document_id=artifact_id, feedback_text=raw_feedback, submitted_by=user_id, feedback_type="revision", project_id=project_id)
        logger.info("[Step 5] Original feedback saved")

        # Step 4: apply rewrites
        suggestions = []
        for sec_id, entries in feedback_map.items():
            sec_record = latest_sections.get(sec_id)
            current_text = sec_record.text if sec_record else ""

            for entry in entries:
                rewritten = self.section_rewriter.run_tool({
                    "section_id": sec_id,
                    "memory": memory,
                    "feedback": entry["text"],
                    "revision_type": entry["type"],
                    "current_text": current_text,
                    **inputs
                })
                log_tool_usage("section_rewriter", "revised section", rewritten, session_id, user_id, inputs)
                trace.append({"tool": "section_rewriter", "output": rewritten})
                logger.info(f"[Step 6.x] section_rewriter complete for {sec_id}")

                save_result = save_artifact_and_trace(
                    section_id=sec_id,
                    artifact_id=artifact_id,
                    gate_id=inputs.get("gate_id", "0"),
                    text=rewritten["draft"],
                    sources=rewritten.get("prompt_used"),
                    tool_outputs=trace,
                    user_id=user_id,
                    project_id=project_id,
                    session_id=session_id
                )
                logger.info(f"[Step 7.x] Saved to ArtifactSection and ReasoningTrace for section {sec_id}")

                if "additional_suggestions" in rewritten:
                    suggestions.append(rewritten["additional_suggestions"])

                # Generate diff summary between original and revised text
                diff_summary = self.diff_summarizer.run_tool({
                    "original": current_text,
                    "revised": rewritten["draft"]
                })
                trace.append({"tool": "diff_summarizer", "output": diff_summary})
                logger.info(f"[Step 8.x] Generated diff summary for section {sec_id}")

                # Compose Redis payload and store to cache revised section + diff summary + metadata
                revision_data = {
                    "text": rewritten["draft"],
                    "diff_summary": diff_summary["diff_summary"],
                    "status": "revised"
                }
                redis_key = f"section_revision:{project_id}:{artifact_id}:{sec_id}"
                redis_client.set(redis_key, json.dumps(revision_data), ex=3600)
                logger.info(f"[Redis] Cached revision data for section {sec_id} under key {redis_key}") 

        logger.info("[Step 9] All sections processed and saved")
        
        return {
            "status": "complete",
            "instructions": (
                "The feedback was processed and changes were applied to relevant sections.\n"
                "You can now review each revised section using `section_review_fetcher`.\n"
                "If additional edits are needed, call `reviseSectionDraft` with specific feedback.\n"
                "Once all updates are confirmed, call `finalizeArtifact` to assemble the revised document."
            ),
            "revised_sections": list(feedback_map.keys())
        }