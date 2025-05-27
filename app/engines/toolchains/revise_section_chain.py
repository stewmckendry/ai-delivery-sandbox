import logging
from app.tools.tool_registry import ToolRegistry
from app.engines.memory_sync import save_artifact_and_trace, log_tool_usage, save_feedback
from app.db.database import get_session
from app.db.models.ArtifactSection import ArtifactSection

logger = logging.getLogger(__name__)

class ReviseSectionChain:
    def __init__(self):
        registry = ToolRegistry()
        self.memory_tool = registry.get_tool("memory_retrieve")
        self.feedback_mapper = registry.get_tool("feedback_mapper")
        self.section_rewriter = registry.get_tool("section_rewriter")
        self.manual_edit_tool = registry.get_tool("manualEditSync")

    def run(self, inputs):
        trace = []
        artifact = inputs.get("artifact")
        section = inputs.get("section")
        feedback = inputs.get("feedback_text")
        mode = inputs.get("mode")  # rewrite, polish, append, verbatim
        session_id = inputs.get("session_id")
        user_id = inputs.get("user_id")
        project_id = inputs.get("project_id")

        memory_input = {**inputs}
        memory = self.memory_tool.run_tool(memory_input)
        log_tool_usage("memory_retrieve", "retrieved memory", memory, session_id, user_id, inputs)
        trace.append({"tool": "memory_retrieve", "output": memory})
        logger.info("[Step 1] memory_retrieve complete")

        # Fetch current section text
        db = get_session()
        section_record = db.query(ArtifactSection).filter_by(artifact_id=artifact, section_id=section).order_by(ArtifactSection.timestamp.desc()).first()
        current_text = section_record.text if section_record else ""

        # Save feedback to FeedbackLog (via handler)
        save_feedback(document_id=artifact, feedback_text=feedback, submitted_by=user_id, feedback_type="revision", project_id=project_id)

        if mode == "verbatim":
            output = self.manual_edit_tool.run_tool({**inputs, "current_text": current_text})
            log_tool_usage("manualEditSync", "accepted user override", output, session_id, user_id, inputs)
            trace.append({"tool": "manualEditSync", "output": output})
            logger.info("[Step 2] manualEditSync complete")
        else:
            section_ids = [section]
            if not section:
                map_result = self.feedback_mapper.run_tool({"feedback_text": feedback, **inputs})
                section_ids = map_result.get("section_ids", [])
                trace.append({"tool": "feedback_mapper", "output": map_result})
                logger.info("[Step 2] feedback_mapper complete")

            for sec_id in section_ids:
                rewritten = self.section_rewriter.run_tool({
                    "section_id": sec_id,
                    "memory": memory,
                    "feedback": feedback,
                    "revision_type": mode,
                    "current_text": current_text,
                    **inputs
                })
                log_tool_usage("section_rewriter", "revised section", rewritten, session_id, user_id, inputs)
                trace.append({"tool": "section_rewriter", "output": rewritten})
                logger.info(f"[Step 3] section_rewriter complete for {sec_id}")

                save_result = save_artifact_and_trace(
                    section_id=sec_id,
                    artifact_id=artifact,
                    gate_id=inputs.get("gate_id", "0"),
                    text=rewritten["draft"],
                    sources=rewritten.get("prompt_used"),
                    tool_outputs=trace,
                    user_id=user_id,
                    project_id=project_id
                )
                logger.info("[Step 4] Saved to ArtifactSection and ReasoningTrace")

        return {"trace": trace, "status": "complete"}